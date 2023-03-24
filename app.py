from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import exc

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class Course(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    school = db.Column(db.String) # e.g "CSE"
    number = db.Column(db.Integer) # e.g. 106
    name = db.Column(db.String) # e.g. "Exploratory Computing"
    instructor = db.Column(db.String) # e.g. "Amon Hepsworth"
    time = db.Column(db.String) # e.g. "TR 3:00PM - 4:15PM"
    currentEnrollment = db.Column(db.Integer) # e.g. 4 (/10)
    maxEnrollment = db.Column(db.Integer) # e.g. 10 (4/)

# DESIGN QUESTIONS
# should Course->Instructor be the Instructor's ID instead?
# should Course->Time be split into Days of Week / Time?
# should Grades belong to Course or Student, or both?
# should Enrollment belong to Course or Student, or both?

class Student():
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String)

class Instructor():
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String)

with app.app_context():
   db.create_all()

@app.get("/")
def index():
    return render_template("index.html")
