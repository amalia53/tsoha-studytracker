from app import app
from flask import Flask, render_template, redirect, request, session
from os import getenv


import users, student, teacher

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	pw = request.form["password"]
	login = users.login(username, pw)
	if login == "invalid_username":
		return render_template("invalid.html", invalid = "käyttäjätunnus")
	elif login == "invalid_pw":
		return render_template("invalid.html", invalid = "salasana")
	elif login == "teacher":
		session["username"] = username
		session["role"] = "teacher"
		return redirect("/teacher")
	else:
		session["username"] = username
		session["role"] = "student"
		return redirect("/student")

@app.route("/logout")
def logout():
	del session["username"]
	session["logged_in"] = False
	return redirect("/")

@app.route("/stureg")
def stu_reg():
        return render_template("student_reg.html")

@app.route("/teachreg")
def teach_reg():
        return render_template("teacher_reg.html")

@app.route("/welcomestudent", methods=["POST"])
def welcome_stu():
	username = request.form["username"]
	registeration = users.student_reg(username, request.form["password"], request.form["verification"])
	if  registeration == "ok":
		return render_template("welcome.html", username = username)
	elif registeration == "no_match":
		return render_template("reg_failed.html", error = "salasanat eivät täsmänneet", role = "student")
	else:
		return render_template("reg_failed.html", error = "käyttäjänimi on jo käytössä",  role = "student")

@app.route("/welcometeacher", methods=["POST"])
def welcome_teacher():
	username = request.form["username"]
	registeration = users.teacher_reg(username, request.form["name"], request.form["password"], request.form["verification"], request.form["code"])
	if  registeration == "ok":
		return render_template("welcome.html", username = username)
	elif registeration == "no_match":
		return render_template("reg_failed.html", error = "salasanat eivät täsmänneet",  role = "teacher")
	elif registeration == "not_authenticated":
		return render_template("reg_failed.html", error = "väärä tunnistautumiskoodi", role = "teacher")
	else:
		return render_template("reg_failed.html", error = "käyttäjänimi on jo käytössä", role = "teacher")

@app.route("/student")
def student_page():
	if session["username"]:
		username = session["username"]
		studentcourses = student.get_students_ongoing_courses(username)
		goals = student.get_students_ongoing_goals(username)
		studied = student.get_students_ongoing_studies(username)
		done = student.get_done(studentcourses, goals, studied)
		return render_template("student.html", studentcourses = studentcourses, goals = goals, studied = studied, done = done)
	else:
		return render_template("notallowed.html")
	
@app.route("/study")
def study():
	if session["username"]:
		courses = student.get_students_ongoing_courses(session["username"])
		courses.sort()
		return render_template("study.html", courses = courses)
	else:
		return render_template("notallowed.html")
	
@app.route("/studied", methods=["POST"])
def studied():
	student.update_studies(session["username"], request.form["course"], request.form["studied"])
	return redirect ("/study")
	
@app.route("/stats")
def stats():
	if session["username"]:
		username = session["username"]
		studentcourses = student.get_students_courses(username)
		goals = student.get_students_goals(username)
		studied = student.get_students_studies(username)
		done = student.get_done(studentcourses, goals, studied)
		completed = student.get_completed(username)
		return render_template("stats.html", studentcourses = studentcourses, goals = goals, studied = studied, done = done, completed = completed)
	else:
		return render_template("notallowed.html")
	
@app.route("/plan")
def plan():
	if session["username"]:
		username = session["username"]
		courses = student.get_courses_student_has_not_added(username)
		studentcourses = student.get_students_ongoing_courses(username)
		goals = student.get_students_ongoing_goals(username)
		studied = student.get_students_ongoing_studies(username)
		done = student.get_done(studentcourses, goals, studied)
		courses.sort()
		return render_template("plan.html", courses = courses, studentcourses = studentcourses, goals = goals, studied = studied, done = done)
	else:
		return render_template("notallowed.html")
	
@app.route("/startcourse", methods=["POST"])
def start_course():
	student.start_course(request.form["course"], request.form["goal"], session["username"])
	return redirect("/plan")

@app.route("/coursedone", methods=["POST"])
def course_done():
	student.complete_course(request.form["course"], session["username"])
	return redirect("/plan")
	
@app.route("/changegoal", methods=["POST"])
def change_goal():
	student.change_plan(request.form["course"], request.form["goal"], session["username"])
	return redirect("/plan")
	
@app.route("/deletefromplan", methods=["POST"])
def delete_from_plan():
	student.delete_from_plan(request.form["course"], session["username"])
	return redirect("/plan")
	
@app.route("/teacher")
def teacher_page():
	if session["role"] == "teacher":
		return render_template("teacher.html")
	else:
		return render_template("notallowed.html")

@app.route("/grade")
def grade():
	courses = teacher.get_teachers_ongoing_courses(session["username"])
	courses.sort()
	return render_template("grade.html", courses = courses)
	
@app.route("/selectcourse", methods=["POST"])
def select_course():
	session["course"] = request.form["course"]
	return redirect("/gradecourse")
	
@app.route("/gradecourse")
def grade_course():
	students = teacher.get_students_from_course(session["course"])
	return render_template("grade_course.html", students = students)
	
@app.route("/addgrade", methods=["POST"])
def add_grade():
	teacher.add_grade(request.form["student"], session["course"], request.form["grade"])
#	return redirect("/gradecourse")
	return render_template("notallowed.html")

@app.route("/graded", methods=["POST"])
def graded():
	del session["course"]
	return redirect("/grade")
	
@app.route("/courses")
def courses_page():
	if session["username"]:
		courses = teacher.get_courses()
		courses.sort()
		return render_template("courses.html", courses = courses)
	else:
		return render_template("notallowed.html")
	
@app.route("/courseadded", methods=["POST"])
def course_added():
	if session["role"] == "teacher":
		teacher.add_course(request.form["course"], session["username"])
	else:
		student.add_course(request.form["course"])
	return redirect("/courses")

