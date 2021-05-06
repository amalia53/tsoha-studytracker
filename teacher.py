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
	return result.fetchone()
	
def get_teachers_ongoing_courses(username):
	teacher_id = get_teacher_id(username)[0]
	sql = "SELECT course FROM courses WHERE teacher_id=:teacher_id"
	result = db.session.execute(sql, {"teacher_id":teacher_id})
	return result.fetchall()

def get_students_from_course(course):
	course_id = student.get_course_id(course)
	sql = "SELECT user_id FROM goals WHERE course_id=:course_id"
	result = db.session.execute(sql, {"course_id":course_id})
	return result.fetchall()

def add_grade(student, course, grade):
	course_id = student.get_course_id(course)
	print(course_id)
	sql = "UPDATE goals SET grade=:grade WHERE user_id=:user_id AND course_id=:course_id"
	db.session.execute(sql, {"grade":grade, "course_id":course_id, "user_id":student})
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
