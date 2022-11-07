from app import api, db
from flask_restful import Resource
from flask import request
from models.models import Plant as PlantsModel
from models.models import Employee as EmployeesModel


class PlantsResource(Resource):
    def get(self):
        filter = request.args
        query = PlantsModel.query
        if len(filter) < 1:
            plants = query.all()
        else:
            for key in filter.keys():
                plants = query.filter(getattr(PlantsModel, key) == filter.get(key))
        plants_data = []
        for plant in plants:
            plants_data.append(plant.serialize())
        return plants_data

    def post(self):
        data = request.json
        plant = PlantsModel(
            title=data.get("title"),
            location=data.get("location")
        )
        db.session.add(plant)
        db.session.commit()
        return plant.serialize()


class SinglePlantResource(Resource):
    def get(self, id):
        plant = PlantsModel.query.get(id)
        return plant.serialize()

    def put(self, id):
        data = request.json
        plant = PlantsModel.query.get(id)
        plant.title = data.get("title", plant.title)
        plant.location = data.get("location", plant.location)
        db.session.add(plant)
        db.session.commit()
        return plant.serialize()

    def delete(self, id):
        plant = PlantsModel.query.get(id)
        employees = EmployeesModel.query.all()
        for employee in employees:
            if employee.plant_id == plant.id:
                return {"you need delete:": employee.serialize()}
        db.session.delete(plant)
        db.session.commit()
        return {"plant": "delete"}


api.add_resource(PlantsResource, "/api/v1/plants")
api.add_resource(SinglePlantResource, "/api/v1/plants/<int:id>")
