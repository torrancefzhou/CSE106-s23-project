from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# will likely need flask-user, flask-login flask-admin
# from sqlalchemy import exc # for specific errors, not sure if needed

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
# probably more

class Student(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String)

class Instructor(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String)

class Account(db.Model): # TODO: username, password, etc
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    type = db.Column(db.String(1), nullable=False) # 's'tudent, 'i'nstructor, 'a'dmin
    roleID = db.Column(db.Integer, nullable=False) # student with id#1, etc

with app.app_context():
    # db.drop_all() # resets tables between instances, do this if you change table models
    db.create_all()

app.secret_key = 'change this later, you need this to run flask-admin'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='gradebook', template_mode='bootstrap3')
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Instructor, db.session))
admin.add_view(ModelView(Account, db.session))

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/classes") # complies with example table in Lab8.pdf, should change later
def get_all_courses():
    json = {}
    for c in Course.query.all():
        json.update({"name": c.school + str(c.number) + ": " + c.name, \
                     "instructor": c.instructor, \
                     "time": c.time, \
                     "enrollment": str(c.enrollment) + "/" + str(c.maxEnrollment) \
                     })
    return json

@app.post("/add")
def add_course():
    pass

@app.post("/drop")
def drop_course():
    pass


