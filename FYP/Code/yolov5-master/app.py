from flask import Flask, jsonify
from flask_cors import CORS  # Remove in production
import config as cfg
from flask_sqlalchemy import SQLAlchemy
from model import db, Userpass, Grid, History  # Importing models
import Weed_Crop_Detect
import datetime
import numpy as np
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS (cross-origin requests)
CORS(app, resources={r'/*': {'origins': '*'}})

# SQL Configuration. Change from config.py
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://@{cfg.dbconfig["host"]}/{cfg.dbconfig["dbname"]}?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# APIs


@app.route('/login/<username>/<password>')
def login(username, password):
    status = 'Login - Fail'
    # Access database
    record = Userpass.query.filter_by(Username=f'{username}').first()
    if not(record):
        status = "404: Login - User not found"
    else:
        userId = record.id
        status = "200: Login - Success" if (record.Password) == (
            password) else "401: Login - Incorrect Password"
    if (status != "200: Login - Success"):
        userId = None

    result = {
        "UserId": userId,
        "Status": str(status)
    }
    print(status)
    return jsonify(result)


@app.route('/signup/<username>/<password>')
def signup(username, password):
    status = '400: Signup - Fail'
    # Access database
    record = Userpass.query.filter_by(Username=f'{username}').first()
    if not(record):
        newUser = Userpass(Username=username, Password=password)
        db.session.add(newUser)
        db.session.commit()
        status = "200: Signup - Success"
    else:
        userId = None
        status = "409: Signup - User Exist"

    result = {
        "Username": username,
        "status": str(status)
    }
    print(status)
    return jsonify(result)


@app.route('/main_menu')
def main_menu():
    status = '400: Main Menu - Fail'
    # Access all records
    record = Grid.query.all()
    if (record):
        status = "200: Main Menu - Success"
        result = []
        for i in record:
            data = {
                "GridID": i.id,
                "Gridname": i.Name,
                "Crop": i.Crop,
                "Src": ""
            }
            result.append(data)
    print(status)
    return jsonify(result)


@app.route('/detect/<path>')
def detect(path):
    status = '400: Detect - Fail'
    # Start detection
    result = Weed_Crop_Detect.main(path)
    if (result):
        status = "200: Detect - Success"
    print(status)
    return jsonify(result)


@app.route('/post_history/<userId>/<gridId>/<Midpoint>')
def post_history(userId, gridId, Midpoint):
    status = '400: Post_History - Fail'
    # Update DB
    newHistory = History(UserID=userId, GridID=gridId,
                         Record_Time=datetime.datetime.utcnow(), Midpoints=Midpoint)
    db.session.add(newHistory)
    db.session.commit()
    status = "200: Post_History - Success"
    return jsonify(status)


@app.route('/get_history/<userId>')
def get_history(userId):
    status = '400: Get_History - Empty'
    # Get user's history
    record = History.query.filter_by(UserID=f'{userId}').all()
    result = []
    if (record):
        status = "200: Get_History - Success"

        midpoint_pairs = []
        for i in record:
            # Process midpoints
            midpoint_array = i.Midpoints.split(",")
            data = {
                "HistoryID": i.id,
                "UserID": i.UserID,
                "GridID": i.GridID,
                "Record_Time": i.Record_Time,
                "Midpoint": midpoint_array
            }

            result.append(data)
    print(status)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
