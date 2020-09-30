from functools import wraps
from pymongo import MongoClient
from bson import ObjectId
from flask import *
app = Flask(__name__)
app.secret_key= 'rutgersIsADeadMeme'
SESSION_TYPE = 'redis'
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
#hrm
client = MongoClient('mongodb://admin:admin@cluster0-shard-00-00-avps1.mongodb.net:27017,cluster0-shard-00-01-avps1.mongodb.net:27017,cluster0-shard-00-02-avps1.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true', 27017)

santa = client['santa-db']
user = []

# Sends static files (JS/CSS) over.
@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html', error=error)
    if request.method == 'POST':
        user = santa['user']
        email = request.form['Email']
        pw = request.form['Password']
        loginUser = user.find_one({'Email' : email, 'Password' : pw})
        if loginUser is None:
            error = "Invalid Credentials, Make sure you are registered and then try again."
        else:
            session['Email'] = email
            return redirect(url_for('dashboard', Email=email))
    print(error)
    return render_template('login.html', error=error)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        user = santa['user']
        email = request.form['Email']
        loginUser = user.find_one({'Email' : email})
        if loginUser is None:
            usr = {
                "Email": email,
                "Name": request.form['Name'],
                "Password": request.form['Password'],
                "Gift": request.form['Gift'],
            }
            user_coll = santa['user']
            user_coll.insert_one(usr)
            flash("Added User")
            return redirect(url_for('login'))
        flash('Email already in Use!')
        return redirect(url_for('login'))
    elif request.method == 'GET':
        user = santa['user']
        print(list(user.find()))
        return render_template('register.html')

@app.route("/dashboard/<Email>", methods=["GET", "POST", "DELETE"])
def dashboard(Email):
    if request.method == "GET":
        if Email not in session['Email']:
            flash('Login First!')
            return redirect(url_for('login'))
        return render_template('dashboard.html')
    elif request.method == "DELETE":
        user = santa['user']
        user.delete_one({"Email": Email})
        return 'done'
    elif request.method == "POST":
        print("aaa")
        session.pop('Email', None)
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)
