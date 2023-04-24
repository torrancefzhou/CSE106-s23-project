from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
from flask_admin.menu import MenuLink
from flask_login import current_user, login_user, login_required, LoginManager, UserMixin, logout_user

from sqlalchemy import inspect

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.secret_key = 'super secret key'
app.app_context().push()
db = SQLAlchemy(app)


class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    is_teacher = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    teaching = db.relationship('Courses', backref='account')
    enrollment = db.relationship('Grades', backref='account')

    def __repr__(self):
        return '<Account %r>' % self.username

    def check_password(self, password):
        return self.password == password


class Courses(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    name = db.Column(db.String) # e.g. "CSE 100"
    time = db.Column(db.String) # e.g. "TR 3:00PM - 4:15PM"
    currentEnrollment = db.Column(db.Integer) # e.g. 4 (/10)
    maxEnrollment = db.Column(db.Integer) # e.g. (4/) 10
    instructor_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False) # e.g. "1001"
    #instructor = db.relationship('Account', backref=db.backref('teacher', lazy=True))

    grades = db.relationship('Grades', backref='courses')

    def __repr__(self):
        return '<Course %r>' % self.name


class Grades(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    grade = db.Column(db.Integer)



with app.app_context():
    # db.drop_all() # resets tables between instances, do this if you change table models
    db.create_all()


class AccountModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = ['id', 'username', 'name', 'is_teacher', 'is_admin']

    def is_accessible(self):
        #return True  # to make new account after resetting DB
        return current_user.get_id() and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class CourseModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Courses).mapper.column_attrs]

    def is_accessible(self):
        #return True  # to make new account after resetting DB
        return current_user.get_id() and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class GradeModelView(sqla.ModelView):
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(Grades).mapper.column_attrs]

    def is_accessible(self):
        #return True  # to make new account after resetting DB
        return current_user.get_id() and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated

class LoginMenuLink(MenuLink):

    def is_accessible(self):
        return not current_user.is_authenticated

admin = Admin(app, name='gradebook', template_mode='bootstrap3')
admin.add_view(AccountModelView(Account, db.session))
admin.add_view(CourseModelView(Courses, db.session))
admin.add_view(GradeModelView(Grades, db.session))
admin.add_link(LoginMenuLink(name='Return to Login Page', category='', url="/login"))
admin.add_link(LogoutMenuLink(name='Return to Homepage', category='', url="/index"))
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))

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
        return render_template('admin_index.html')
    elif current_user.is_teacher:
        return render_template('teacher_index.html')
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

@app.route('/class', methods=['GET'])
@login_required
def getClass():
    if current_user.is_teacher:
        data = Courses.query.filter_by(instructor_id=current_user.id).all()
        #teacher = Account.query.filter_by(id=data.instructor_id)
        return jsonify([{"name": item.name,
                     "instructor": current_user.name,
                     "time": item.time,
                     "currentEnrollment": item.currentEnrollment,
                     "maxEnrollment": item.maxEnrollment} for item in data])
    else:
        classid = Grades.query.filter_by(student_id=current_user.id).all()
        data = Account.query.filter_by(username='missing').all()
        for x in classid:
            temp = Courses.query.filter_by(id=x.class_id).first()
            data.append(temp)

        return jsonify([{"name": item.name,
                     "instructor": (Account.query.filter_by(id=item.instructor_id).first()).name,
                     "time": item.time,
                     "currentEnrollment": item.currentEnrollment,
                     "maxEnrollment": item.maxEnrollment} for item in data])

@app.route('/classes', methods=['GET'])
@login_required
def getAllClass():
    data = Courses.query.all()

    return jsonify([{"name": item.name,
                     "instructor": (Account.query.filter_by(id=item.instructor_id).first()).name,
                     "time": item.time,
                     "currentEnrollment": item.currentEnrollment,
                     "maxEnrollment": item.maxEnrollment,
                     "enrolled": Grades.query.filter_by(class_id=item.id, student_id=current_user.id).count() > 0} for item in data])


@app.route("/class/<course>", methods=['GET'])
@login_required
def inClass(course):
    classid = (Courses.query.filter_by(name=course).first()).id
    studentgrades = Grades.query.filter_by(class_id=classid, student_id=current_user.id).all()
    if (studentgrades is None):
        return "False"
    else:
        return "True"


@app.route("/classes/<course>", methods=['GET'])
@login_required
def getGrade(course):
    temp = Courses.query.filter_by(name=course).first()
    data = Grades.query.filter_by(class_id=temp.id).all()
    return jsonify([{"student": (Account.query.filter_by(id=item.student_id).first()).name,
                     "grade": item.grade} for item in data])

@app.route("/classes/<course>", methods=['PUT'])
@login_required
def editGrade(course):
    classid = (Courses.query.filter_by(name=course).first()).id
    classgrades = Grades.query.filter_by(class_id=classid).all()
    body = request.get_json()
    print("Student name from request:", body['name'])
    student = Account.query.filter_by(name=body['name']).first()
    if student:
        studentid = student.id
        studentgrade = [g for g in classgrades if g.student_id == studentid][0]
        studentgrade.grade = body['grade']
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route("/classes/<course>", methods=['POST'])
@login_required
def addStudent(course):
    find_course = Courses.query.filter_by(name=course).first()

    # check enrollment of student
    enrollment = Grades.query.filter_by(student_id=current_user.id, class_id=find_course.id).count()
    if enrollment > 0:
        return 'Already enrolled in '+course+''

    # add student to course
    newStudent = Grades(student_id=current_user.id, class_id=find_course.id, grade=0)
    find_course.currentEnrollment += 1
    db.session.add(newStudent)
    db.session.commit()
    return 'Enrolled in '+course+''


@app.route("/classes/<course>", methods=['DELETE'])
@login_required
def dropStudent(course):
    find_course = Courses.query.filter_by(name=course).first()
    classid = find_course.id
    grade_obj = Grades.query.filter_by(student_id=current_user.id, class_id=classid).first()
    if grade_obj:
        db.session.delete(grade_obj)
        find_course.currentEnrollment -= 1
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')


if __name__ == "__main__":
    app.run()