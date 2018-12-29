import json
from pymongo import MongoClient
from bson import ObjectId
from flask import Flask, request
app = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

santa_db = client['santa-db']

users = []

@app.route("/users", methods=["POST", "GET"])
def user_list():
    if request.method == 'GET':
        user_coll = santa_db['user']
        print(list(users_coll.find()))
        return JSONEncoder().encode(list(user_coll.find()))
    else:
        user = {
            "UserName": request.get_json()['UserName'],
            "Name": request.get_json()['Name'],
            "Password": request.get_json()['Password'],
            "Gift": request.get_json()['Gift']
        }
        user_coll = santa_db['user']
        user_coll.insert_one(usr)
        return "FINSHED INSERTION."
