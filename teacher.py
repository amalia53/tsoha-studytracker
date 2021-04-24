from db import db

def get_teacher_name(username):
	sql = "SELECT name FROM teachers WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone()
	
def get_teacher_id(name):
	sql = "SELECT id FROM teachers WHERE name=:name"
	result = db.session.execute(sql, {"name":name})
	return result.fetchone()
	
def add_course(course, teacher):
	teacher_id = get_teacher_id(teacher)
	sql = "INSERT INTO courses (course, teacher_id) VALUES (:course, :teacher_id)"
	db.session.execute(sql, {"course":course, "teacher_id":teacher_id})
	db.session.commit()
	
def get_courses():
	result = db.session.execute("SELECT course FROM courses")
	return result.fetchall()
