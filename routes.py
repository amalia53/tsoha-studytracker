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
		return redirect("/teacher")
	else:
		session["username"] = username
		return redirect("/student")

@app.route("/logout")
def logout():
	del session["username"]
	return redirect("/")

@app.route("/stureg")
def stu_reg():
        return render_template("student_reg.html")

@app.route("/teachreg")
def teach_reg():
        return render_template("teacher_reg.html")

@app.route("/welcomestudent", methods=["POST"])
def welcome_stu():
	registeration = users.student_reg(request.form["username"], request.form["password"], request.form["verification"])
	if  registeration == "ok":
		return render_template("welcome.html", username = username)
	elif registeration == "no_match":
		return render_template("reg_failed.html", error = "salasanat eivät täsmänneet", role = "student")
	else:
		return render_template("reg_failed.html", error = "käyttäjänimi on jo käytössä",  role = "student")

@app.route("/welcometeacher", methods=["POST"])
def welcome_teacher():
	name = request.form["name"]
	registeration = users.teacher_reg(request.form["username"], name, request.form["password"], request.form["verification"], request.form["code"])
	if  registeration == "ok":
		return render_template("welcome.html", username = name)
	elif registeration == "no_match":
		return render_template("reg_failed.html", error = "salasanat eivät täsmänneet",  role = "teacher")
	elif registeration == "not_authenticated":
		return render_template("reg_failed.html", error = "väärä tunnistautumiskoodi", role = "teacher")
	else:
		return render_template("reg_failed.html", error = "käyttäjänimi on jo käytössä", role = "teacher")

@app.route("/student")
def student_page():	
	username = session["username"]
	studentcourses = student.get_students_ongoing_courses(username)
	goals = student.get_students_ongoing_goals(username)
	studied = student.get_students_ongoing_studies(username)
	done = student.get_done(studentcourses, goals, studied)
	return render_template("student.html", studentcourses = studentcourses, goals = goals, studied = studied, done = done)
	
@app.route("/study")
def study():
	courses = student.get_students_ongoing_courses(session["username"])
	courses.sort()
	return render_template("study.html", courses = courses)
	
@app.route("/studied", methods=["POST"])
def studied():
	student.update_studies(session["username"], request.form["course"], request.form["studied"])
	return redirect ("/study")
	
@app.route("/stats")
def stats():
	username = session["username"]
	studentcourses = student.get_students_courses(username)
	goals = student.get_students_goals(username)
	studied = student.get_students_studies(username)
	done = student.get_done(studentcourses, goals, studied)
	completed = student.get_completed(username)
	return render_template("stats.html", studentcourses = studentcourses, goals = goals, studied = studied, done = done, completed = completed)
	
@app.route("/plan")
def plan():	
	username = session["username"]
	courses = student.get_courses_student_has_not_added(username)
	studentcourses = student.get_students_ongoing_courses(username)
	goals = student.get_students_ongoing_goals(username)
	studied = student.get_students_ongoing_studies(username)
	done = student.get_done(studentcourses, goals, studied)
	courses.sort()
	return render_template("plan.html", courses = courses, studentcourses = studentcourses, goals = goals, studied = studied, done = done)
	
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
	return render_template("teacher.html")

@app.route("/grade")
def grade():
	return render_template("grade.html")
	
@app.route("/courses")
def courses_page():
	courses = teacher.get_courses()
	courses.sort()
	role = users.get_user_role(session["username"])
	return render_template("courses.html", courses = courses, role = role)
	
@app.route("/courseadded", methods=["POST"])
def course_added():
	if is_teacher(session["username"]):
		teacher.add_course(request.form["course"], session["username"])
	else:
		student.add_course(request.form["course"])
	return redirect("/courses")

