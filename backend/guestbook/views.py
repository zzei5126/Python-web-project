import hashlib
import json
import logging

from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .charts import build_chart
from .forms import EntryForm
from .models import Entry
from .services import create_entry, delete_entry, statistics

logger = logging.getLogger(__name__)


@require_GET
def index(request):
    entries = list(Entry.objects.all())
    return render(request, "index.html", {"entries": entries})


@require_http_methods(["GET", "POST"])
def add(request):
    form = EntryForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        if form.is_valid():
            try:
                create_entry(form.cleaned_data)
                messages.success(request, "Đã thêm lời nhắn thành công!")
                return redirect("index")
            except Exception:
                logger.exception("Lỗi khi lưu lời nhắn")
                form.add_error(None, "Không thể lưu lời nhắn. Vui lòng thử lại.")
        return render(request, "add.html", {"form": form}, status=400)
    return render(request, "add.html", {"form": form})


@require_http_methods(["GET", "POST"])
def delete(request, id):
    try:
        delete_entry(id)
        messages.success(request, "Đã xóa lời nhắn.")
    except Exception:
        logger.exception("Lỗi khi xóa lời nhắn")
        messages.error(request, "Không thể xóa lời nhắn.")
    return redirect("index")


@require_GET
def stats(request):
    data = statistics()
    fingerprint = hashlib.md5(
        json.dumps(data["senders"], ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()[:10]
    data["chart_version"] = fingerprint
    return render(request, "stats.html", data)


@require_GET
def chart_image(request):
    data = statistics()
    fingerprint = hashlib.md5(
        json.dumps(data["senders"], ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()[:10]

    etag = f'"{fingerprint}"'
    if request.headers.get("If-None-Match") == etag:
        return HttpResponse(status=304)

    path = build_chart(data["senders"])
    response = FileResponse(path.open("rb"), content_type="image/png")
    response["Cache-Control"] = "public, max-age=3600"
    response["ETag"] = etag
    return response
