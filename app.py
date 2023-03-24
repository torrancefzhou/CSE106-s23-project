from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import exc

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

# class Grade(db.Model):
#    name = db.Column(db.String, unique=True, primary_key=True, nullable=False)
#    grade = db.Column(db.Float, nullable=False)
# with app.app_context():
#    db.create_all()

@app.get("/")
def index():
    return render_template("index.html")
