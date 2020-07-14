import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from db import db
from es_helper import ESHelper
from user import UserModel
from security import authenticate, identity

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

class UserRegister(Resource):
    '''
    /register endpoint implementation
    accepts, registers username and password
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="Username cannot be blank.")
    parser.add_argument('password', type=str, required=True,
                        help="Password cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class AppStatus(Resource):
    '''
    /health_check endpoint implementation
    gets status from Elasticsearch; returns App status
    '''
    def get(self):
        app_status = ESHelper.get_status()
        for service in app_status:
            if app_status[service] == "DOWN":
                return {"appstatus": "DOWN"}
        return {"appstatus": "UP"}

class IndividualServiceStatus(Resource):
    '''
    /health_check/rbcapp1 endpoint implementation
    gets status from Elasticsearch;
    returns App status along with inidividual service status
    '''
    def get(self):
        app_status = ESHelper.get_status()
        for service in app_status:
            if app_status[service] == "DOWN":
                app_status['rbcapp1'] = "DOWN"
                return app_status
        app_status['rbcapp1'] = "UP"
        return app_status

class UpdateStatus(Resource):
    '''
    /add endpoint implementation
    accepts one or more files, stores them in Elasticsearch
    '''
    @jwt_required()
    def post(self):
        results = []
        uploadedfile = request.files
        for file in uploadedfile:
            request_data = json.load(uploadedfile[file])
            index = request_data["service_name"]
            update_response = ESHelper.update_status(index, request_data)
            if not update_response:
                return {"upload_status": "Failed"}, 500
            results.append(update_response["result"])
        results_set = set(results)
        if "updated" in results_set or "created" in results_set:
            return {"upload_status": "Success"}
        return {"upload_status": "Failed"}, 500

api.add_resource(AppStatus, '/health_check')
api.add_resource(IndividualServiceStatus, '/health_check/rbcapp1')
api.add_resource(UpdateStatus, '/add')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run()
