#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        return {"message": "Welcome to the plant database"}


api.add_resource(Home, "/")


class Plants(Resource):
    pass

    def get(self):
        response = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(response, 200)

    def post(self):
        data = request.get_json() if request.is_json else request.form
        plant = Plant(**data)
        db.session.add(plant)
        db.session.commit()
        return make_response(plant.to_dict(), 201, {"Content-Type": "application/json"})


api.add_resource(Plants, "/plants")


class PlantByID(Resource):
    pass

    def get(self, id):
        response = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(response, 200)


api.add_resource(PlantByID, "/plants/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)