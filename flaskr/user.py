# 회원가입, 로그인, 마이 페이지

from flask import Blueprint, flash, render_template, redirect, request, session, url_for
from flask_login import login_user, login_required, logout_user
from bs4 import BeautifulSoup
from random import randint
import requests
from .util import bc, db, User

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/register1", methods=["GET", "POST"])
def register1():
    if request.method == "GET":
        return render_template("register1.html")

    username = request.form.get("username").strip()  # type: ignore
    if User.query.filter_by(username=username).first():
        flash("이미 존재하는 아이디입니다.")
        return redirect(url_for("user_bp.register1"))

    code = []
    for _ in range(10):
        code.append(chr(randint(97, 122)))

    session["register_username"] = username
    session["register_code"] = "".join(code)
    session["register_verified"] = False
    return redirect(url_for("user_bp.register2"))


@user_bp.route("/register2", methods=["GET", "POST"])
def register2():
    if "register_username" not in session:
        flash("회원가입 세션이 만료되었습니다. 다시 시도하세요.")
        return redirect(url_for("user_bp.register1"))
    username = session["register_username"]
    code = session["register_code"]
    print(code)

    if request.method == "GET":
        return render_template("register2.html", username=username, code=code)

    response = requests.get(f"https://koistudy.net/user_profile?id={username}")
    soup = BeautifulSoup(response.text, "html.parser")
    h1 = soup.select_one("div.profile-container h1").get_text()  # type: ignore
    if "(" in h1:
        name = h1[h1.find("(") + 1 : -8]
    else:
        name = ""
    print(name)

    if code == name:
        session["register_verified"] = True
        return redirect(url_for("user_bp.register3"))

    flash("계정 인증에 실패했습니다. 다시 시도하세요.")
    return redirect(url_for("user_bp.register2"))


@user_bp.route("/register3", methods=["GET", "POST"])
def register3():
    if "register_username" not in session:
        flash("회원가입 세션이 만료되었습니다. 다시 시도하세요.")
        return redirect(url_for("user_bp.register1"))
    if not session.get("register_verified"):
        flash("계정 인증에 실패했습니다. 다시 시도하세요.")
        return redirect(url_for("user_bp.register2"))

    if request.method == "GET":
        return render_template("register3.html")

    password = request.form["password"]
    hash = bc.generate_password_hash(password).decode("utf-8")

    user = User(username=session["register_username"], password=hash)  # type: ignore
    db.session.add(user)
    db.session.commit()

    session.pop("register_username", None)
    session.pop("register_code", None)
    session.pop("register_verified", None)

    flash("회원가입이 완료되었습니다.")
    return redirect(url_for("user_bp.login"))


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("아이디가 존재하지 않습니다. 다시 시도하세요.")
        return redirect(url_for("user_bp.login"))

    password = request.form["password"]
    if bc.check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for("home"))
    else:
        flash("비밀번호가 일치하지 않습니다. 다시 시도하세요.")
        return redirect(url_for("user_bp.login"))


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
