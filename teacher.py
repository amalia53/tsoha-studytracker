from db import db

import users, student

def add_teacher(name, user_id):
	sql = "INSERT INTO teachers (name, user_id) VALUES (:name, :user_id)"
	result = db.session.execute(sql, {"name":name, "user_id":user_id})
	db.session.commit()

def get_teacher_id(username):
	user_id = users.get_user_id(username)[0]
	sql = "SELECT id FROM teachers WHERE user_id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id})
	teacher_id = result.fetchone()[0]
	return teacher_id
	
def get_teachers_ongoing_courses(username):
	teacher_id = get_teacher_id(username)
	sql = "SELECT course FROM courses WHERE teacher_id=:teacher_id"
	result = db.session.execute(sql, {"teacher_id":teacher_id})
	return result.fetchall()

def get_students_from_course(course):
	course_id = student.get_course_id(course)
	sql = "SELECT user_id FROM goals WHERE course_id=:course_id AND NOT deleted AND grade IS NULL"
	result = db.session.execute(sql, {"course_id":course_id})
	return result.fetchall()

def get_ongoing_courses_table(username):
	teacher_id = get_teacher_id(username)
	sql = "SELECT course, id FROM courses WHERE teacher_id=:teacher_id"
	result = db.session.execute(sql, {"teacher_id":teacher_id})
	results = result.fetchall()
	counts = []
	courses = []
	for course in results:
		sql = "SELECT COUNT(*) FROM goals WHERE course_id=:course_id AND NOT deleted"
		result = db.session.execute(sql, {"course_id":course[1]})
		count = result.fetchone()
		courses.append(course[0])
		counts.append(count[0])
	return courses, counts

def add_grade(student_id, course, grade):
	course_id = student.get_course_id(course)
	sql = "UPDATE goals SET grade=:grade WHERE user_id=:user_id AND course_id=:course_id AND NOT deleted"
	db.session.execute(sql, {"grade":grade, "course_id":course_id, "user_id":student_id})
	db.session.commit()
	
def add_course(course, username):
	teacher_id = get_teacher_id(username)[0]
	sql = "INSERT INTO courses (course, teacher_id) VALUES (:course, :teacher_id)"
	db.session.execute(sql, {"course":course, "teacher_id":teacher_id})
	db.session.commit()
	
def get_courses():
	result = db.session.execute("SELECT course FROM courses")
	courses = result.fetchall()
	courses.sort()
	return courses
