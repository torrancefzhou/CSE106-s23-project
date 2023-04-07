from flask import Flask, redirect, url_for, request, render_template
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, login_required, LoginManager, UserMixin, logout_user

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    is_teacher = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def check_password(self, password):
        return self.password == password


class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    instructor = db.relationship('Courses', backref=db.backref('classes', lazy=True))

    def __repr__(self):
        return '<Category %r>' % self.name


class Courses(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String) # e.g. "CSE 100"
    time = db.Column(db.String) # e.g. "TR 3:00PM - 4:15PM"
    currentEnrollment = db.Column(db.Integer) # e.g. 4 (/10)
    maxEnrollment = db.Column(db.Integer) # e.g. 10 (4/)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False) # e.g. "1001"

    def __repr__(self):
        return '<Category %r>' % self.name


enrollment = db.Table('enrollment',
    db.Column('student_id', db.Integer, db.ForeignKey('account.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True),
    db.Column('grade', db.Integer, nullable=False)
)


with app.app_context():
    # db.drop_all() # resets tables between instances, do this if you change table models
    db.create_all()

class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


admin = Admin(app, name='gradebook', template_mode='bootstrap3')
admin.add_view(MyModelView(Account, db.session))
admin.add_view(MyModelView(Courses, db.session))
admin.add_view(MyModelView(Instructor, db.session))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)

@app.route('/index')
@app.route('/')
@login_required
def index(): # put application's code here
    if current_user.is_admin:
        return render_template('gradebook-home.html')
    elif current_user.is_teacher:
        return render_template('teacher_home.html')
    else:
        return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = Account.query.filter_by(username=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        return redirect(url_for('login'))
    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

@app.route("/book")
@login_required
def indexfull():
    return render_template('gradebook-home.html')

@app.route("/class/<user>")
@login_required
def classTable(user):
    if user.is_teacher:
        return user.classes
    else:
        return enrollment.query.filter_by(student_id=user.id).all()

if __name__ == "__main__":
    app.run()

