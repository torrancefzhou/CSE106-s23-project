from flask import Flask, redirect, url_for, request, render_template
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, login_required, LoginManager, UserMixin, logout_user

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

    def check_password(self, password):
        return self.password == password

class Course(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String) # e.g. "Exploratory Computing"
    instructor = db.Column(db.String) # e.g. "Amon Hepsworth"
    time = db.Column(db.String) # e.g. "TR 3:00PM - 4:15PM"
    currentEnrollment = db.Column(db.Integer) # e.g. 4 (/10)
    maxEnrollment = db.Column(db.Integer) # e.g. 10 (4/)

class Enrollment(db.Model):
    studentid = db.Column(db.Integer)
    classid = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)

class Instruction(db.Model):
    classid = db.Column(db.Integer)
    teacherid = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)

with app.app_context():
    # db.drop_all() # resets tables between instances, do this if you change table models
    db.create_all()

admin = Admin(app, name='gradebook', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Enrollment, db.session))
admin.add_view(ModelView(Instruction, db.session))
#admin.add_view(ModelView(Account, db.session))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/index')
@app.route('/')
@login_required
def index(): # put application's code here
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

if __name__ == "__main__":
    app.run()

