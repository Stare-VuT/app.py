from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, create_user, get_user, verify_user

app = Flask(__name__)
app.secret_key = "supersecretkey123"

init_db()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = verify_user(username, password)

        if not user:
            flash("Sai tài khoản hoặc mật khẩu!", "error")
            return redirect(url_for("login"))

        if user["banned"] == 1:
            flash("Tài khoản của bạn đã bị khóa!", "error")
            return redirect(url_for("login"))

        session["user"] = user["username"]
        session["role"] = user["role"]
        flash("Đăng nhập thành công!", "success")
        return redirect(url_for("home"))

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

        if get_user(username):
            flash("Tên tài khoản đã tồn tại!", "error")
            return redirect(url_for("register"))

        success = create_user(username, password)

        if success:
            flash("Đăng ký thành công! Hãy đăng nhập.", "success")
            return redirect(url_for("login"))
        else:
            flash("Đăng ký thất bại!", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/home")
def home():
    if "user" not in session:
        flash("Bạn cần đăng nhập trước!", "error")
        return redirect(url_for("login"))

    return render_template(
        "home.html",
        username=session["user"],
        role=session.get("role", "user")
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
