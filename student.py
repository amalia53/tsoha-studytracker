from db import db

def course_done(student, course):
	course_id = get_course_id()
	student_id = get_student_id()
	sql = "UPDATE studentcourses SET ongoing=:ongoing WHERE student_id=:student_id AND course_id=:course_id""
	db.session.execute(sql, {"ongoing":false})
	db.session.commit()

def get_student_id(username):
	sql = "SELECT id FROM students WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone()

def get_course_id(course):
	sql = "SELECT id FROM courses WHERE course=:course"
	result = db.session.execute(sql, {"course":course})
	return result.fetchone()
