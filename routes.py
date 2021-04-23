from app import app
from db import db
from flask import Flask, render_template, redirect, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

import users

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	pw = request.form["password"]
	if users.login == "invalid_username":
		return render_template("invalid.html", invalid = "käyttäjätunnus")
	elif users.login == "invalid_pw":
		return render_template("invalid.html", invalid = "salasana")

	else:
		return redirect("/student")


@app.route("/logout")
def logout():
    del users.get_session()
    return redirect("/")

@app.route("/stureg")
def stu_reg():
        return render_template("student_reg.html")

@app.route("/teachreg")
def teach_reg():
        return render_template("teacher_reg.html")

@app.route("/welcome", methods=["POST"])
def welcome():
	username = request.form["username"]
	sql = "SELECT username FROM students WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if user == None:
		pw = request.form["password"]
		verification = request.form["verification"]
		if pw == verification:
			hash_pw = generate_password_hash(pw)
			sql = "INSERT INTO students (username, pw) VALUES (:username, :pw)"
			db.session.execute(sql, {"username":username, "pw":hash_pw})
			db.session.commit()
			return render_template("welcome.html", username = username)
		else:
			return render_template("reg_failed.html", error = "salasanat eivät täsmänneet")
	else:
		return render_template("reg_failed.html", error = "käyttäjänimi on jo käytössä")
		

@app.route("/student")
def student():	
	username = get_session()
	studentcourses = get_students_courses(username)
	goals = get_students_goals(username)
	studied = get_students_studies(username)
	done = get_done(studentcourses, goals, studied)
	
	return render_template("student.html", studentcourses = studentcourses, goals = goals, studied = studied, done = done)
	
@app.route("/study")
def study():
	courses = get_students_courses(session["username"])
	courses.sort()
	return render_template("study.html", courses = courses)
	
@app.route("/studied", methods=["POST"])
def studied():
	course = request.form["course"]
	studied = request.form["studied"]
	update_studies(session["username"], course, studied)
	return redirect ("/study")
	
@app.route("/stats")
def stats():
	return render_template("stats.html")
	
@app.route("/plan")
def plan():	
	username = session["username"]
	
	courses = get_courses_student_has_not_added(username)
	studentcourses = get_students_courses(username)
	goals = get_students_goals(username)
	studied = get_students_studies(username)
	done = get_done(studentcourses, goals, studied)
	courses.sort()
	return render_template("plan.html", courses = courses, studentcourses = studentcourses, goals = goals, studied = studied, done = done)
	
@app.route("/startcourse", methods=["POST"])
def start_course():
	course = request.form["course"]
	goal = request.form["goal"]
	course_id = get_course_id(course)
	student_id = get_student_id(session["username"])
	sql = "INSERT INTO goals (student_id, course_id, goal, studied) VALUES (:student_id, :course_id, :goal, :studied)"
	db.session.execute(sql, {"student_id":student_id[0], "course_id":course_id[0], "goal":goal, "studied":0})
	db.session.commit()
	return redirect("/plan")
	
@app.route("/courses")
def courses():
	result = db.session.execute("SELECT course FROM courses")
	courses = result.fetchall()
	courses.sort()
	return render_template("courses.html", courses = courses)
	
@app.route("/courseadded", methods=["POST"])
def course_added():
	course = request.form["course"]
	teacher = request.form["teacher"]
	sql = "INSERT INTO courses (course, teacher) VALUES (:course, :teacher)"
	db.session.execute(sql, {"course":course, "teacher":teacher})
	db.session.commit()
	return redirect("/courses")
	
def get_student_id(username):
	sql = "SELECT id FROM students WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone()
	
def get_course_id(course):
	sql = "SELECT id FROM courses WHERE course=:course"
	result = db.session.execute(sql, {"course":course})
	return result.fetchone() 
	
def get_students_courses(username):
	student_id = get_student_id(username)
	sql = "SELECT course FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.student_id=:student_id"
	result = db.session.execute(sql, {"student_id":student_id[0]})
	studentcourses = result.fetchall()
	return studentcourses

def get_courses_student_has_not_added(username):
	student_id = get_student_id(username)
	sql = "SELECT course FROM courses WHERE NOT id IN (SELECT course_id FROM goals WHERE student_id=:student_id)"
	result = db.session.execute(sql, {"student_id":student_id[0]})
	return result.fetchall()

def get_students_goals(username):
	student_id = get_student_id(username)
	sql = "SELECT goal FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.student_id=:student_id"
	result = db.session.execute(sql, {"student_id":student_id[0]})
	return result.fetchall()
	
def get_students_studies(username):
	student_id = get_student_id(username)
	sql = "SELECT studied FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.student_id=:student_id"
	result = db.session.execute(sql, {"student_id":student_id[0]})
	return result.fetchall() 

def get_done(studentcourses, goals, studied):
	done = []
	rng = len(studentcourses)
	for i in range(rng):
		prosent = (studied[i][0] / goals[i][0]) * 100
		prosent = int(prosent)
		done.append(prosent)
	return done
	
def update_studies(username, course, studied):
	student_id = get_student_id(username)
	course_id = get_course_id(course)
	studied = int(studied)
	studied_pre = get_previous_studies(username, course, student_id, course_id)[0]	
	studied += studied_pre
	print(studied)
	sql = "UPDATE goals SET studied=:studied WHERE student_id=:student_id AND course_id=:course_id"
	result = db.session.execute(sql, {"studied":studied, "course_id":course_id[0], "student_id":student_id[0]})
	db.session.commit()

def get_previous_studies(username, course, student_id, course_id):
	sql = "SELECT studied FROM goals WHERE student_id=:student_id AND course_id=:course_id"
	result = db.session.execute(sql, {"course_id":course_id[0], "student_id":student_id[0]})
	return result.fetchone()

