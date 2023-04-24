from app import db, Account, Courses, Grades

# Account
student1 = Account(username = "student1", password = "student1", name = "Jose Santos", is_teacher=False, is_admin=False)
student2 = Account(username = "student2", password = "student2", name = "Betty Brown", is_teacher=False, is_admin=False)
student3 = Account(username = "student3", password = "student3", name = "John Stuart", is_teacher=False, is_admin=False)
student4 = Account(username = "student4", password = "student4", name = "Li Cheng", is_teacher=False, is_admin=False)
student5 = Account(username = "student5", password = "student5", name = "Nancy Little", is_teacher=False, is_admin=False)
student6 = Account(username = "student6", password = "student6", name = "Mindy Norris", is_teacher=False, is_admin=False)
student7 = Account(username = "student7", password = "student7", name = "Aditya Ranganath", is_teacher=False, is_admin=False)
student8 = Account(username = "student8", password = "student8", name = "Yi Wen Chen", is_teacher=False, is_admin=False)

teacher1 = Account(username = "teach1", password = "teach1", name = "Ralph Jenkins", is_teacher=True, is_admin=False)
teacher2 = Account(username = "teach2", password = "teach2", name = "Susan Walker", is_teacher=True, is_admin=False)
teacher3 = Account(username = "teach3", password = "teach3", name = "Ammon Hepworth", is_teacher=True, is_admin=False)

admin = Account(username = "admin", password = "admin", name = "admin", is_teacher=False, is_admin=True)


# course
course1 = Courses(name = "Math 101",
                  time = "MWF 10:00-10:50 AM",
                  currentEnrollment = 4,
                  maxEnrollment = 8,
                  instructor_id = (Account.query.filter_by(username = "teach1").first()).id)

course2 = Courses(name = "Physics 121",
                  time = "TR 11:00-11:50 AM",
                  currentEnrollment = 5,
                  maxEnrollment = 10,
                  instructor_id = (Account.query.filter_by(username = "teach2").first()).id)

course3 = Courses(name = "CS 106",
                  time = "MWF 2:00-2:50 PM",
                  currentEnrollment = 4,
                  maxEnrollment = 10,
                  instructor_id = (Account.query.filter_by(username = "teach3").first()).id)

course4 = Courses(name = "CS 162",
                  time = "TR 3:00-3:50 PM",
                  currentEnrollment = 4,
                  maxEnrollment = 4,
                  instructor_id = (Account.query.filter_by(username = "teach3").first()).id)

# Grade
grade11 = Grades(student_id = (Account.query.filter_by(name = "Jose Santos").first()).id,
                class_id = (Courses.query.filter_by(name = "Math 101").first()).id,
                grade = 92)
grade12 = Grades(student_id = (Account.query.filter_by(name = "Betty Brown").first()).id,
                class_id = (Courses.query.filter_by(name = "Math 101").first()).id,
                grade = 65)
grade13 = Grades(student_id = (Account.query.filter_by(name = "John Stuart").first()).id,
                class_id = (Courses.query.filter_by(name = "Math 101").first()).id,
                grade = 86)
grade14 = Grades(student_id = (Account.query.filter_by(name = "Li Cheng").first()).id,
                class_id = (Courses.query.filter_by(name = "Math 101").first()).id,
                grade = 77)

grade21 = Grades(student_id = (Account.query.filter_by(name = "Nancy Little").first()).id,
                class_id = (Courses.query.filter_by(name = "Physics 121").first()).id,
                grade = 53)
grade22 = Grades(student_id = (Account.query.filter_by(name = "Li Cheng").first()).id,
                class_id = (Courses.query.filter_by(name = "Physics 121").first()).id,
                grade = 85)
grade23 = Grades(student_id = (Account.query.filter_by(name = "Mindy Norris").first()).id,
                class_id = (Courses.query.filter_by(name = "Physics 121").first()).id,
                grade = 94)
grade24 = Grades(student_id = (Account.query.filter_by(name = "John Stuart").first()).id,
                class_id = (Courses.query.filter_by(name = "Physics 121").first()).id,
                grade = 91)
grade25 = Grades(student_id = (Account.query.filter_by(name = "Betty Brown").first()).id,
                class_id = (Courses.query.filter_by(name = "Physics 121").first()).id,
                grade = 88)

grade31 = Grades(student_id = (Account.query.filter_by(name = "Aditya Ranganath").first()).id,
                class_id = (Courses.query.filter_by(name = "CS 106").first()).id,
                grade = 93)
grade32 = Grades(student_id = (Account.query.filter_by(name = "Yi Wen Chen").first()).id,
                class_id = (Courses.query.filter_by(name = "CS 106").first()).id,
                grade = 85)
grade33 = Grades(student_id = (Account.query.filter_by(name = "Nancy Little").first()).id,
                class_id = (Courses.query.filter_by(name = "CS 106").first()).id,
                grade = 57)
grade34 = Grades(student_id = (Account.query.filter_by(name = "Mindy Norris").first()).id,
                class_id = (Courses.query.filter_by(name = "CS 106").first()).id,
                grade = 68)

grade41 = Grades(student_id = (Account.query.filter_by(name = "Aditya Ranganath").first()).id,
                class_id = (Courses.query.filter_by(name = "CS 162").first()).id,
                grade = 99)
grade42 = Grades(student_id = (Account.query.filter_by(name = "Nancy Little").first()).id,
                class_id = (Courses.query.filter_by(name = "CS 162").first()).id,
                grade = 87)
grade43 = Grades(student_id = (Account.query.filter_by(name = "Yi Wen Chen").first()).id,
                class_id = (Courses.query.filter_by(name = "CS 162").first()).id,
                grade = 92)
grade44 = Grades(student_id = (Account.query.filter_by(name = "John Stuart").first()).id,
                class_id = (Courses.query.filter_by(name = "CS 162").first()).id,
                grade = 67)


# add
#db.session.add(student1)
#db.session.add(student2)
#db.session.add(student3)
#db.session.add(student4)
#db.session.add(student5)
#db.session.add(student6)
#db.session.add(student7)
#db.session.add(student8)
#db.session.add(teacher1)
#db.session.add(teacher2)
#db.session.add(teacher3)
#db.session.add(admin)
#db.session.add(course1)
#db.session.add(grade1)
#db.session.add(instruction1)
#db.session.add(course1)
#db.session.add(course2)
#db.session.add(course3)
#db.session.add(course4)
#db.session.add(grade11)
#db.session.add(grade12)
#db.session.add(grade13)
#db.session.add(grade14)
#db.session.add(grade21)
#db.session.add(grade22)
#db.session.add(grade23)
#db.session.add(grade24)
#db.session.add(grade25)
#db.session.add(grade31)
#db.session.add(grade32)
#db.session.add(grade33)
#db.session.add(grade34)
#db.session.add(grade41)
#db.session.add(grade42)
#db.session.add(grade43)
#db.session.add(grade44)

# delete
# User.query.filter_by(username = "test").delete()
# Course.query.filter_by(name = "Exploratory Computing").delete()
# Enrollment.query.filter_by(studentid = 123).delete()
# Instruction.query.filter_by(classid = 456).delete()

db.session.commit()