from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"

USERS_FILE = "users.json"

# Tạo file users.json nếu chưa có
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        users = load_users()

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                flash("Đăng nhập thành công!", "success")
                return redirect(url_for("home"))

        flash("Sai tài khoản hoặc mật khẩu!", "error")
        return redirect(url_for("login"))

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        confirm = request.form["confirm"].strip()

        if not username or not password or not confirm:
            flash("Vui lòng nhập đầy đủ thông tin!", "error")
            return redirect(url_for("register"))

        if password != confirm:
            flash("Mật khẩu xác nhận không khớp!", "error")
            return redirect(url_for("register"))

        users = load_users()

        for user in users:
            if user["username"] == username:
                flash("Tên tài khoản đã tồn tại!", "error")
                return redirect(url_for("register"))

        users.append({
            "username": username,
            "password": password
        })

        save_users(users)
        flash("Đăng ký thành công! Hãy đăng nhập.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/home")
def home():
    if "user" not in session:
        flash("Bạn cần đăng nhập trước!", "error")
        return redirect(url_for("login"))

    return render_template("home.html", username=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Bạn đã đăng xuất.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
