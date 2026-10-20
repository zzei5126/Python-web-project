import json
import os
import tempfile
from pathlib import Path

from django.conf import settings
from django.db import connection, transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404
from filelock import FileLock

from .models import Entry


def _data_path():
    path = Path(settings.DATA_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _save_json():
    rows = list(Entry.objects.order_by("id").values("id", "name", "message", "created_at"))
    path = _data_path()
    encoded = json.dumps(rows, ensure_ascii=False, indent=2, default=lambda v: v.isoformat()).encode("utf-8")
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".gb-", delete=False) as f:
            tmp = Path(f.name)
            f.write(encoded)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if tmp:
            tmp.unlink(missing_ok=True)


def reindex_entries():
    entries = list(Entry.objects.order_by("id"))
    for i, entry in enumerate(entries, start=1):
        if entry.id != i:
            Entry.objects.filter(pk=entry.pk).update(id=i)
    if connection.vendor == "sqlite":
        with connection.cursor() as cursor:
            cursor.execute("UPDATE sqlite_sequence SET seq = %s WHERE name = 'guestbook_entry'", [len(entries)])


def create_entry(data):
    with FileLock(str(_data_path()) + ".lock", timeout=15):
        with transaction.atomic():
            entry = Entry.objects.create(**data)
            _save_json()
    return entry


def delete_entry(entry_id):
    with FileLock(str(_data_path()) + ".lock", timeout=15):
        with transaction.atomic():
            entry = get_object_or_404(Entry, pk=entry_id)
            entry.delete()
            reindex_entries()
            _save_json()


def statistics():
    senders = list(
        Entry.objects.values("name")
        .annotate(count=Count("id"))
        .order_by("-count", "name")
    )
    return {
        "total_entries": sum(s["count"] for s in senders),
        "total_senders": len(senders),
        "top_senders": senders[:5],
        "senders": senders,
    }


def load_json_into_db():
    path = _data_path()
    if not path.exists() or Entry.objects.exists():
        return
    with FileLock(str(path) + ".lock", timeout=15):
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            return
        with transaction.atomic():
            for row in rows:
                if isinstance(row, dict) and row.get("name") and row.get("message"):
                    Entry.objects.create(
                        name=row["name"][:100],
                        message=row["message"][:2000],
                    )
            reindex_entries()
        _save_json()
