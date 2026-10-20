import json
import os
import base64
from datetime import datetime
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "guestbook-secret-key-2024"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


def load_entries():
    """Doc danh sach loi nhan tu file JSON khi khoi dong."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_entries(entries):
    """Ghi danh sach loi nhan ra file JSON de luu tru lau dai."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def next_id(entries):
    """Sinh ID tu tang an toan (khong bi trung ke ca sau khi xoa)."""
    if not entries:
        return 1
    return max(e["id"] for e in entries) + 1


# ── Route / (GET) ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    """
    Buoi 1: Lay danh sach tat ca loi nhan va render index.html.
    Truyen bien `entries` vao template.
    """
    entries = load_entries()
    entries_sorted = sorted(entries, key=lambda e: e["id"], reverse=True)
    return render_template("index.html", entries=entries_sorted)


# ── Route /add (GET, POST) ─────────────────────────────────────────────────────
@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Buoi 1:
    GET : Hien thi form nhap name + message.
    POST: Validate -> luu -> redirect / hoac render lai form voi loi.
    """
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()
        # Validate: khong de trong ca hai truong
        if not name and not message:
            error = "Vui long nhap ca ten va loi nhan."
        elif not name:
            error = "Vui long nhap ten cua ban."
        elif not message:
            error = "Vui long nhap loi nhan."
        else:
            entries = load_entries()
            new_entry = {
                "id": next_id(entries),
                "name": name,
                "message": message,
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            entries.append(new_entry)
            save_entries(entries)
            flash("Loi nhan cua ban da duoc gui thanh cong!", "success")
            return redirect(url_for("index"))
        # Neu loi: render lai form voi thong bao loi
        return render_template("add.html", error=error, name=name, message=message)
    # GET: hien thi form trong
    return render_template("add.html", error=None, name="", message="")


# ── Route /delete/<int:id> (POST hoac GET) ────────────────────────────────────
@app.route("/delete/<int:entry_id>", methods=["POST", "GET"])
def delete(entry_id):
    """
    Buoi 1: Xoa entry co ID tuong ung, sau do redirect ve /.
    """
    entries = load_entries()
    original_len = len(entries)
    entries = [e for e in entries if e["id"] != entry_id]
    if len(entries) < original_len:
        save_entries(entries)
        flash("Da xoa loi nhan so " + str(entry_id), "info")
    else:
        flash("Khong tim thay loi nhan so " + str(entry_id), "warning")
    return redirect(url_for("index"))


# ── Route /stats (GET) ────────────────────────────────────────────────────────
@app.route("/stats")
def stats():
    """
    Buoi 2: Hien thi thong ke:
      - Tong so loi nhan
      - Top 5 nguoi gui nhieu nhat
      - Bieu do cot bang Matplotlib -> nhung vao HTML dang base64
    """
    entries = load_entries()
    total = len(entries)
    name_counter = Counter(e["name"] for e in entries)
    top5 = name_counter.most_common(5)

    chart_b64 = None
    if top5:
        names = [t[0] for t in top5]
        counts = [t[1] for t in top5]

        # Ve bieu do cot bang Matplotlib
        fig, ax = plt.subplots(figsize=(8, 4.5))
        fig.patch.set_facecolor("#0F172A")
        ax.set_facecolor("#1E293B")

        palette = ["#6C63FF", "#7C3AED", "#EC4899", "#06B6D4", "#10B981"]
        colors = palette[:len(names)]

        bars = ax.bar(names, counts, color=colors, edgecolor="none", width=0.55, zorder=3)

        for bar, cnt in zip(bars, counts):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                str(cnt),
                ha="center", va="bottom",
                color="#E2E8F0", fontsize=11, fontweight="bold"
            )

        ax.set_title("Top nguoi gui loi nhan", color="#E2E8F0",
                     fontsize=14, fontweight="bold", pad=14)
        ax.set_xlabel("Nguoi gui", color="#94A3B8", fontsize=10, labelpad=8)
        ax.set_ylabel("So loi nhan", color="#94A3B8", fontsize=10, labelpad=8)
        ax.tick_params(colors="#94A3B8")
        ax.spines[:].set_visible(False)
        ax.yaxis.grid(True, color="#334155", linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        plt.tight_layout(pad=1.5)

        # Luu tam thanh file PNG trong static/
        os.makedirs(STATIC_DIR, exist_ok=True)
        chart_path = os.path.join(STATIC_DIR, "stats.png")
        plt.savefig(chart_path, dpi=130, facecolor=fig.get_facecolor())
        plt.close(fig)

        # Encode sang base64 de nhung thang vao HTML
        with open(chart_path, "rb") as img_file:
            chart_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    return render_template("stats.html", total=total, top5=top5, chart_b64=chart_b64)


if __name__ == "__main__":
    os.makedirs(STATIC_DIR, exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
