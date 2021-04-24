from db import db

def add_course(course, teacher):
	teacher_id = teacher.get_teacher_id(teacher)
	sql = "INSERT INTO courses (course, teacher_id) VALUES (:course, :teacher_id)"
	db.session.execute(sql, {"course":course, "teacher_id":teacher_id})
	db.session.commit()
	
def get_courses():
	result = db.session.execute("SELECT course FROM courses")
	courses = result.fetchall()
	courses.sort()
	return courses
