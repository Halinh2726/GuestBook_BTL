import base64
import json
import os
from collections import Counter
from datetime import datetime
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"

app = Flask(__name__)
app.secret_key = os.environ.get("GUESTBOOK_SECRET", "guestbook-local-development-key")


def load_entries():
    """Read guestbook entries and recover gracefully from an invalid data file."""
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8-sig"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_entries(entries):
    """Persist entries without leaving a half-written JSON file behind."""
    temporary_file = DATA_FILE.with_suffix(".tmp")
    temporary_file.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temporary_file.replace(DATA_FILE)


def next_id(entries):
    return max((entry.get("id", 0) for entry in entries), default=0) + 1


def make_chart(top_authors):
    """Return an on-brand, transparent PNG chart as a base64 string."""
    if not top_authors:
        return None

    names = [item[0] for item in reversed(top_authors)]
    counts = [item[1] for item in reversed(top_authors)]
    colors = ["#d9dfd0", "#c9d5bf", "#9fbd9b", "#5d8c68", "#ff6b4a"][-len(names) :]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    bars = ax.barh(names, counts, color=colors, height=0.54)

    for bar, count in zip(bars, counts):
        ax.text(
            count + max(counts) * 0.035,
            bar.get_y() + bar.get_height() / 2,
            str(count),
            va="center",
            color="#15251d",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_xlim(0, max(counts) * 1.25)
    ax.set_xticks([])
    ax.tick_params(axis="y", colors="#4c5b53", labelsize=11, length=0, pad=12)
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout(pad=1.4)

    image = BytesIO()
    plt.savefig(image, format="png", dpi=160, transparent=True, bbox_inches="tight")
    plt.close(fig)
    image.seek(0)
    return base64.b64encode(image.read()).decode("utf-8")


@app.route("/")
def index():
    entries = sorted(load_entries(), key=lambda entry: entry.get("id", 0), reverse=True)
    unique_authors = len({entry.get("name", "") for entry in entries})
    return render_template(
        "index.html", entries=entries, unique_authors=unique_authors
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    name = ""
    message = ""
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not message:
            error = "Vui lòng nhập đầy đủ tên và lời nhắn."
        elif len(name) > 80:
            error = "Tên không được dài quá 80 ký tự."
        elif len(message) > 500:
            error = "Lời nhắn không được dài quá 500 ký tự."
        else:
            entries = load_entries()
            entries.append(
                {
                    "id": next_id(entries),
                    "name": name,
                    "message": message,
                    "timestamp": datetime.now().strftime("%d/%m/%Y · %H:%M"),
                }
            )
            save_entries(entries)
            flash("Lời nhắn đã được lưu vào cuốn sổ.", "success")
            return redirect(url_for("index"))

    return render_template("add.html", error=error, name=name, message=message)


@app.post("/delete/<int:entry_id>")
def delete(entry_id):
    entries = load_entries()
    updated_entries = [entry for entry in entries if entry.get("id") != entry_id]

    if len(updated_entries) == len(entries):
        flash("Không tìm thấy lời nhắn cần xóa.", "warning")
    else:
        save_entries(updated_entries)
        flash("Đã xóa lời nhắn khỏi cuốn sổ.", "info")
    return redirect(url_for("index"))


@app.route("/stats")
def stats():
    entries = load_entries()
    author_counts = Counter(entry.get("name", "Khuyết danh") for entry in entries)
    top_authors = author_counts.most_common(5)
    latest_entry = max(entries, key=lambda entry: entry.get("id", 0), default=None)

    return render_template(
        "stats.html",
        total=len(entries),
        unique_authors=len(author_counts),
        top_authors=top_authors,
        latest_entry=latest_entry,
        chart_b64=make_chart(top_authors),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
