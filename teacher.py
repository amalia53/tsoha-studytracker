from db import db

import users, student

def add_teacher(name, user_id):
	sql = "INSERT INTO teachers (name, user_id) VALUES (:name, :user_id)"
	result = db.session.execute(sql, {"name":name, "user_id":user_id})
	db.session.commit()

def get_teacher_id(user_id):
	sql = "SELECT id FROM teachers WHERE user_id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id})
	teacher_id = result.fetchone()
	return teacher_id[0]
	
def get_teachers_ongoing_courses(user_id):
	# teacher_id = get_teacher_id(user_id)
	# sql = "SELECT course FROM courses WHERE teacher_id=:teacher_id"
	sql = "SELECT courses.id, course FROM courses, teachers WHERE user_id=:user_id AND teacher_id=teachers.id"
	results = db.session.execute(sql, {"user_id":user_id})
	return student.add_to_arrays_2(results.fetchall())

def get_students_from_course(course_id):
	sql = "SELECT user_id FROM goals WHERE course_id=:course_id AND NOT deleted AND grade IS NULL"
	result = db.session.execute(sql, {"course_id":course_id})
	return result.fetchall()

def get_ongoing_courses_table(user_id):
	teacher_id = get_teacher_id(user_id)
	sql = "SELECT course, id FROM courses WHERE teacher_id=:teacher_id ORDER BY course ASC"
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

def get_stats_table(user_id):
	sql = "SELECT c.id, c.course FROM courses c, teachers t WHERE t.user_id=:user_id AND t.id=c.teacher_id ORDER BY c.course ASC"
	result = db.session.execute(sql, {"user_id":user_id})
	results = result.fetchall()
	courses = []
	counts = []
	grades = []
	studies = []
	for course in results:
		sql = "SELECT AVG(grade), COUNT(user_id), AVG(studied) FROM goals WHERE course_id=:course_id AND NOT deleted"
		result = db.session.execute(sql, {"course_id":course[0]})
		course_results = result.fetchall()
		courses.append(course[1])
		grades.append(course_results[0])
		counts.append(course_results[1])
		studies.append(course_results[2])
	return courses, counts, grades, studied

def add_grade(student_id, course_id, grade):
	sql = "UPDATE goals SET grade=:grade WHERE user_id=:user_id AND course_id=:course_id AND NOT deleted"
	db.session.execute(sql, {"grade":grade, "course_id":course_id, "user_id":student_id})
	db.session.commit()
	
def add_course(course, user_id):
	teacher_id = get_teacher_id(user_id)
	sql = "INSERT INTO courses (course, teacher_id) VALUES (:course, :teacher_id)"
	db.session.execute(sql, {"course":course, "teacher_id":teacher_id})
	db.session.commit()
	
def get_courses():
	result = db.session.execute("SELECT course FROM courses ORDER BY course ASC")
	courses = result.fetchall()
	return courses
