from db import db


def get_student_id(username):
	sql = "SELECT id FROM students WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone()

def get_course_id(course):
	sql = "SELECT id FROM courses WHERE course=:course"
	result = db.session.execute(sql, {"course":course})
	return result.fetchone()
