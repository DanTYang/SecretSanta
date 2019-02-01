import json 
from functools import wraps
from pymongo import MongoClient
from bson import ObjectId
from flask import * 
app = Flask(__name__)
app.secret_key= 'rutgersIsADeadMeme'

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = MongoClient('localhost', 27017)

santa = client['santa-db']
user = []

# Sends static files (JS/CSS) over.
@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")

@app.route("/logout/<Email>", methods=["GET"])
def logout(Email):
    user = santa['user']
    user.update({"Email": Email},{"$set":{"Logged_in": False}})
    flash("You have been logged out!")
    return redirect(url_for('login'))

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        user = santa['user']
        email = request.form['Email']
        pw = request.form['Password']
        loginUser = user.find_one({'Email' : email, 'Password' : pw})
        if loginUser is None:
            error = "Invalid Credentials, Make sure you are registered and then try again."
        else:
            loginUser = user.find_one({'Email' : email, 'Password': pw, 'Logged_in' : True})
            if loginUser:        
                flash("You are already logged in!")
                return redirect(url_for('dashboard', Email=email))    
            else:
                user.update({"Email": email},{"$set":{"Logged_in": True}})
                flash("You have been logged in!")
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
                "Logged_in": True
            }
            user_coll = santa['user']
            user_coll.insert_one(usr)
            flash("Added User")
            return redirect(url_for('login'))
        flash('Email already in Use!')
        return redirect(url_for('register'))
    elif request.method == 'GET':
        user = santa['user']
        print(list(user.find()))
        return render_template('register.html')

@app.route("/dashboard", methods=["GET"])
def get_dashboard():
    email = request.args.get('Email')
    user = santa['user']

    loginUser = user.find_one({'Email': email})

    # if loginUser:
    #     not_logged_in = user.find_one({'Email': email, 'Logged_in': False})
    #     if not_logged_in:
    #         flash("You are not logged in")
    #         return redirect(url_for('login'))
    return render_template('dashboard.html')
    
    # return redirect(url_for('main_page'))

@app.route("/dashboard", methods=["DELETE", "POST"])
def dashboard(Email):
    if request.method == "DELETE":
        user = santa['user']
        user.delete_one({"Email": Email})
        return 'done'
    elif request.method == "POST":
        return redirect(url_for('logout', Email=Email))
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    app.run(debug=False)
