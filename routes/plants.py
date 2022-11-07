from app import app, db
from flask import render_template, request, redirect, session
from models.models import Plant, Employee, User


def session_user():
    user = None
    if session.get("user", False):
        user = User.query.get(session.get("user"))
    return user


@app.route("/add-plant")
def add_plant():
    plants = Plant.query.all()
    employees = Employee.query.all()
    return render_template("add_plant.html", plants=plants, employees=employees, user=session_user())


@app.route("/plants")
def plants():
    plants = Plant.query.all()
    return render_template("plants.html", plants=plants, user=session_user())


@app.route("/save-plant", methods=["POST"])
def save_plant():
    name = request.form.get("name")
    location = request.form.get("location")
    plant = Plant(title=name, location=location)
    db.session.add(plant)
    for employee_id in request.form.getlist("employees"):
        employee = Employee.query.get(int(employee_id))
        employee.plant_id = plant.id
        db.session.add(employee)
    db.session.commit()
    return redirect("/")


@app.route("/info-plant/<int:id>")
def info_plant(id):
    plant = Plant.query.get(id)
    employees = Employee.query.filter(Employee.plant_id == id)
    return render_template("info_plant.html", plant=plant, employees=employees, user=session_user())


@app.route("/delete-plant/<int:id>")
def delete_plant(id):
    plant = Plant.query.get(id)
    employees = Employee.query.all()
    for employee in employees:
        if employee.plant_id == plant.id:
            return redirect("/edit-employee/{}/{}".format(employee.id, 1))
    db.session.delete(plant)
    db.session.commit()
    return redirect("/")


@app.route("/edit-plant/<int:id>")
def edit_plant(id):
    plant = Plant.query.get(id)
    employees = Employee.query.all()
    return render_template("add_plant.html", plant=plant, employees=employees, user=session_user())


@app.route("/update-plant/<int:id>", methods=["POST"])
def update_plant(id):
    plant = Plant.query.get(id)
    plant.title = request.form.get("name")
    plant.location = request.form.get("location")
    db.session.add(plant)
    for employee_id in request.form.getlist("employees"):
        employee = Employee.query.get(int(employee_id))
        employee.plant_id = plant.id
        db.session.add(employee)
    db.session.commit()
    return redirect("/")
