from db import db

import users

def add_teacher(name, user_id):
	sql = "INSERT INTO teachers (name, user_id) VALUES (:name, :user_id)"
	result = db.session.execute(sql, {"name":name, "user_id":user_id})

def get_teacher_id(username):
	user_id = users.get_user_id(username)
	sql = "SELECT id FROM teachers WHERE user_id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id})
	return result.fetchone()
	
def add_course(course, username):
	teacher_id = get_teacher_id(username)
	sql = "INSERT INTO courses (course, teacher_id) VALUES (:course, :teacher_id)"
	db.session.execute(sql, {"course":course, "teacher_id":teacher_id})
	db.session.commit()
	
def get_courses():
	result = db.session.execute("SELECT course FROM courses")
	courses = result.fetchall()
	courses.sort()
	return courses
