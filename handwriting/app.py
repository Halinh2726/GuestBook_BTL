
import json
import os
import base64
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "123456"

DATA_FILE = "data.json"


# Doc du lieu tu file JSON
def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            entries = json.load(f)
            return entries

    return []


# Luu du lieu vao file JSON
def save_entries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)


# Tao ID moi
def next_id(entries):
    max_id = 0

    for entry in entries:
        if entry["id"] > max_id:
            max_id = entry["id"]

    return max_id + 1


# Trang chu - Hien thi danh sach loi nhan
@app.route("/")
def index():
    entries = load_entries()

    entries.sort(key=lambda x: x["id"], reverse=True)

    return render_template("index.html", entries=entries)


# Them loi nhan
@app.route("/add", methods=["GET", "POST"])
def add():
    error = None
    name = ""
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()

        # Kiem tra du lieu nhap
        if name == "" and message == "":
            error = "Vui long nhap ten va loi nhan."

        elif name == "":
            error = "Vui long nhap ten."

        elif message == "":
            error = "Vui long nhap loi nhan."

        else:
            entries = load_entries()

            # Tao loi nhan moi
            new_entry = {
                "id": next_id(entries),
                "name": name,
                "message": message,
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M")
            }

            # Them vao danh sach
            entries.append(new_entry)

            # Luu vao file
            save_entries(entries)

            flash("Them loi nhan thanh cong!", "success")

            return redirect(url_for("index"))

    return render_template(
        "add.html",
        error=error,
        name=name,
        message=message
    )


# Xoa loi nhan theo ID
@app.route("/delete/<int:entry_id>", methods=["GET", "POST"])
def delete(entry_id):
    entries = load_entries()

    new_entries = []
    found = False

    for entry in entries:
        if entry["id"] == entry_id:
            found = True
        else:
            new_entries.append(entry)

    if found:
        save_entries(new_entries)
        flash("Da xoa loi nhan!", "info")
    else:
        flash("Khong tim thay loi nhan!", "warning")

    return redirect(url_for("index"))


# Trang thong ke
@app.route("/stats")
def stats():
    entries = load_entries()

    # Tong so loi nhan
    total = len(entries)

    # Dem so loi nhan cua tung nguoi
    count = {}

    for entry in entries:
        name = entry["name"]

        if name in count:
            count[name] = count[name] + 1
        else:
            count[name] = 1

    # Sap xep theo so loi nhan giam dan
    result = sorted(count.items(), key=lambda x: x[1], reverse=True)

    # Lay 5 nguoi gui nhieu nhat
    top5 = result[:5]

    chart_b64 = None

    if len(top5) > 0:
        names = []
        numbers = []

        for name, number in top5:
            names.append(name)
            numbers.append(number)

        # Ve bieu do cot
        plt.figure(figsize=(8, 4))

        plt.bar(names, numbers, color="skyblue")

        plt.title("Top 5 nguoi gui loi nhan")
        plt.xlabel("Nguoi gui")
        plt.ylabel("So loi nhan")

        plt.tight_layout()

        # Luu bieu do vao file PNG
        os.makedirs("static", exist_ok=True)

        chart_path = "static/stats.png"

        plt.savefig(chart_path)
        plt.close()

        # Chuyen anh sang base64
        with open(chart_path, "rb") as f:
            image_data = f.read()
            chart_b64 = base64.b64encode(image_data).decode("utf-8")

    return render_template(
        "stats.html",
        total=total,
        top5=top5,
        chart_b64=chart_b64
    )


# Chay chuong trinh
if __name__ == "__main__":
    app.run(debug=True)
