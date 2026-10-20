import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from threading import Lock

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from django.conf import settings
from filelock import FileLock
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

matplotlib.rcParams["font.sans-serif"] = ["Segoe UI", "Arial", "DejaVu Sans", "sans-serif"]
matplotlib.rcParams["font.family"] = "sans-serif"

_render_lock = Lock()
_palette = ["#4f46e5", "#6366f1", "#7c3aed", "#8b5cf6", "#06b6d4", "#0ea5e9", "#3b82f6", "#10b981", "#f59e0b", "#ec4899"]


def build_chart(senders):
    directory = Path(settings.CHART_DIR)
    directory.mkdir(parents=True, exist_ok=True)

    static_path = settings.BASE_DIR / "static" / "stats.png"
    static_path.parent.mkdir(parents=True, exist_ok=True)

    fingerprint = hashlib.sha256(
        json.dumps(senders, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()[:16]
    path = directory / f"stats-{fingerprint}.png"

    with FileLock(str(directory / "chart.lock"), timeout=15):
        if path.exists():
            if not static_path.exists():
                shutil.copyfile(path, static_path)
            return path

        with _render_lock:
            n = len(senders)
            fig_width = max(min(n * 1.1 + 3.0, 11.0), 6.5)
            fig = Figure(figsize=(fig_width, 4.4), dpi=180, layout="constrained", facecolor="#ffffff")
            ax = fig.add_subplot(111)
            ax.set_facecolor("#ffffff")

            if senders:
                names = [s["name"] for s in senders]
                counts = [s["count"] for s in senders]
                colors = [_palette[i % len(_palette)] for i in range(n)]
                bar_width = min(0.55, 0.28 + 0.04 * n)

                bars = ax.bar(names, counts, color=colors, width=bar_width, edgecolor="none", zorder=3)
                ax.bar_label(bars, padding=6, fontsize=10, fontweight="bold", color="#1e293b")

                max_count = max(counts)
                ax.set_ylim(0, max_count * 1.28 + 1)
                ax.yaxis.get_major_locator().set_params(integer=True)

                longest_name = max(len(name) for name in names) if names else 0
                if longest_name > 8 or n > 5:
                    ax.tick_params(axis="x", labelrotation=22, labelsize=9.5, pad=6)
                else:
                    ax.tick_params(axis="x", labelrotation=0, labelsize=10, pad=6)

                ax.tick_params(axis="y", labelsize=9.5, left=False)
            else:
                ax.text(0.5, 0.5, "Chưa có dữ liệu lời nhắn", ha="center", va="center", transform=ax.transAxes, fontsize=13, color="#94a3b8", fontweight="500")
                ax.set_xticks([])
                ax.set_yticks([])

            ax.set_ylabel("Số lượng lời nhắn", fontsize=10, fontweight="600", color="#64748b", labelpad=10)
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.spines["bottom"].set_color("#cbd5e1")
            ax.spines["bottom"].set_linewidth(1.0)
            ax.grid(axis="y", linestyle="--", alpha=0.5, color="#cbd5e1", zorder=1)
            ax.set_axisbelow(True)

            tmp = None
            try:
                with tempfile.NamedTemporaryFile(dir=directory, suffix=".png", delete=False) as f:
                    tmp = Path(f.name)
                FigureCanvasAgg(fig).print_png(str(tmp))
                os.replace(tmp, path)
                shutil.copyfile(path, static_path)
            finally:
                if tmp:
                    tmp.unlink(missing_ok=True)
                fig.clear()

        for old in sorted(directory.glob("stats-*.png"), key=lambda p: p.stat().st_mtime, reverse=True)[10:]:
            if old != path:
                old.unlink(missing_ok=True)

    return path
