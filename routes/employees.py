from app import app, db
from flask import render_template, request, redirect, session
from models.models import Employee, Plant, User


def session_user():
    user = None
    if session.get("user", False):
        user = User.query.get(session.get("user"))
    return user


@app.route("/employees")
def employees_home():
    employees = Employee.query.all()
    return render_template("employees-list.html", employees=employees, user=session_user())


@app.route("/add-employee", methods=["POST", "GET"])
def add_Employees():
    if request.method == "POST":
        data = request.form
        try:
            employee = Employee(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                plant_id=int(data.get("plant_id"))
            )
            db.session.add(employee)
            db.session.commit()
        except:
            return "This already exist!"
        return redirect("/employees")
    else:
        plants = Plant.query.all()
        return render_template("add_employee.html", plants=plants, user=session_user())


@app.route("/edit-employee/<int:id>/<int:check>")
def edit_employee(id, check):
    plants = Plant.query.all()
    employee = Employee.query.get(id)
    return render_template("add_employee.html", plants=plants, employee=employee, check=check, user=session_user())


@app.route("/update-employee/<int:id>", methods=["POST"])
def update_employee(id):
    try:
        employee = Employee.query.get(id)
        employee.first_name = request.form.get("first_name")
        employee.last_name = request.form.get("last_name")
        employee.email = request.form.get("email")
        employee.plant_id = request.form.get("plant_id")
        db.session.add(employee)
        db.session.commit()
    except:
        return "This already exist!"
    return redirect("/employees")


# @app.route("/info-plant/<int:id>")
# def info_plant(id):
#     plant = Plant.query.get(id)
#     employees = Employee.query.filter(Employee.plant_id == id)
#     return render_template("info_plant.html", plant=plant, employees=employees)


@app.route("/delete-employee/<int:id>")
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")
