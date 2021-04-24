from app import app
from db import db
from flask import Flask, render_template, redirect, request, session
from os import getenv


import users
import student

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

@app.route("/welcome", methods=["POST"])
def welcome():
	username = request.form["username"]
	registeration = users.student_reg(username, request.form["password"], request.form["verification"])
	if  registeration == "ok":
		return render_template("welcome.html", username = username)
	elif registeration == "no_match":
		return render_template("reg_failed.html", error = "salasanat eivät täsmänneet")
	else:
		return render_template("reg_failed.html", error = "käyttäjänimi on jo käytössä")
		

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

