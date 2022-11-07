from app import app, db
from flask import render_template, request, session, redirect
from sqlalchemy import or_
from models.models import Plant, Employee, User
import hashlib


@app.route("/")
def main():
    plants = Plant.query.all()
    employees = Employee.query.all()
    user = None
    if session.get("user", False):
        user = User.query.get(session.get("user"))
    return render_template("index.html", plants=plants, employees=employees, user=user)


@app.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        data = request.form
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username"),
            email=data.get("email"),
            password=hashlib.md5(data.get("password").encode()).hexdigest()
        )
        db.session.add(user)
        db.session.commit()
        session["user"] = user.id
        return redirect("/")
    else:
        return render_template("sign-up.html")


@app.route("/sign-in", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        user = User.query.filter(or_(User.email == request.form.get("email"),
                                     User.username == request.form.get("email"))).first()
        if user is not None:
            if user.password == hashlib.md5(request.form.get("password").encode()).hexdigest():
                session["user"] = user.id
        return redirect("/")
    else:
        return render_template("sign-in.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


