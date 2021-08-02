from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Userpass(db.Model):
    __tablename__ = 'tbl_Userpass'
    id = db.Column('User_Id', db.Integer, primary_key=True)
    Username = db.Column('Username', db.String)
    Password = db.Column('Password', db.String)

class Grid(db.Model):
    __tablename__ = 'tbl_Grid'
    id = db.Column('Grid_Id', db.Integer, primary_key=True)
    Name = db.Column('Grid_Name', db.String)
    Crop = db.Column('Crop', db.String)

class History(db.Model):
    __tablename__ = 'tbl_History'
    id = db.Column('History_Id', db.Integer, primary_key=True)
    UserID = db.Column('User_Id', db.Integer)
    GridID = db.Column('Grid_Id', db.Integer)
    Record_Time = db.Column('Record_Time', db.DateTime)
    Midpoints = db.Column('Midpoint', db.String)