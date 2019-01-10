import json
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
from flask import Flask, request, render_template, url_for, session, redirect
app = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = MongoClient('localhost', 27017)

santa_db = client['santa-db']

@app.route('/')
def index():
    return redirect(url_for('index')

@app.route("/users", methods=["POST", "GET"])
def user_list():
    if request.method == 'GET':
        user_coll = santa_db['user']
        print(list(user_coll.find()))
        return JSONEncoder().encode(list(user_coll.find()))
    else:
        user = {
            "Email": request.get_json()['Email'],
            "Name": request.get_json()['Name'],
            "Password": request.get_json()['Password'],
            "Gift": request.get_json()['Gift']
        }
        user_coll = santa_db['user']
        user_coll.insert_one(user)
        return "FINSHED INSERTION."

@app.route("/users/<Email>", methods=["GET", "DELETE", "PUT"])
def blog_User_list(Email): 
    if request.method == 'GET':
        user_coll = santa_db['user']
        return JSONEncoder().encode(user_coll.find_one({"Email":Email}))
    elif request.method == 'DELETE':
        user_coll = santa_db['user']
        user_coll.delete_one({"Email": Email})
        return "Deleted User"
    else:
        user_coll = santa_db['user']
        user_coll.update({"Email": Email},{"$set": request.get_json()})
        return "Done"

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
