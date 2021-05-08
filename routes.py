from app import app
from flask import Flask, render_template, redirect, request, session
from os import getenv


import users, student, teacher

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
	username = ""
	if "user_id" in session:
		username = users.get_username(session["user_id"])
	return render_template("index.html", username=username)

@app.route("/login", methods=["POST"])
def login():
	login = users.login(request.form["username"], request.form["password"])
	if login[0] == "invalid":
		if login[1] == "username":
			return render_template("invalid.html", invalid="käyttäjätunnus")
		else:
			return render_template("invalid.html", invalid="salasana")
	else:
		session["user_id"] = login[0]
		if login[1] == "teacher":
			session["role"] = "teacher"
			return redirect("/teacher")
		else:
			session["role"] = "student"
			return redirect("/student")

@app.route("/logout")
def logout():
	if "user_id" in session:
		del session["user_id"]
		del session["role"]
		return redirect("/")
	else:
		return render_template("notallowed.html")
		

@app.route("/stureg")
def stu_reg():
        return render_template("student_reg.html")

@app.route("/teachreg")
def teach_reg():
        return render_template("teacher_reg.html")

@app.route("/welcomestudent", methods=["POST"])
def welcome_stu():
	username = request.form["username"]
	role = "student"
	registeration = users.student_reg(username, request.form["password"], request.form["verification"])
	if  registeration == "ok":
		return render_template("welcome.html", username=username)
	elif registeration == "username_too_short":
		return render_template("reg_failed.html", error="käyttäjätunnus oli alle viisi merkkiä pitkä.", role=role)
	elif registeration == "pw_too_short":
		return render_template("reg_failed.html", error="salasana oli alle kahdeksan merkkiä pitkä.", role=role)
	elif registeration == "no_match":
		return render_template("reg_failed.html", error="salasanat eivät täsmänneet.", role=role)
	else:
		return render_template("reg_failed.html", error="käyttäjänimi on jo käytössä.", role=role)

@app.route("/welcometeacher", methods=["POST"])
def welcome_teacher():
	username = request.form["username"]
	role = "teacher"
	registeration = users.teacher_reg(username, request.form["name"], request.form["password"], request.form["verification"], request.form["code"])
	if  registeration == "ok":
		return render_template("welcome.html", username = username)
	elif registeration == "username_too_short":
		return render_template("reg_failed.html", error="käyttäjätunnus oli alle viisi merkkiä pitkä.", role=role)
	elif registeration == "pw_too_short":
		return render_template("reg_failed.html", error="salasana oli alle kahdeksan merkkiä pitkä.", role=role)
	elif registeration == "no_match":
		return render_template("reg_failed.html", error="salasanat eivät täsmänneet.",  role=role)
	elif registeration == "not_authenticated":
		return render_template("reg_failed.html", error="väärä tunnistautumiskoodi.", role=role)
	else:
		return render_template("reg_failed.html", error="käyttäjänimi on jo käytössä.", role=role)

@app.route("/student")
def student_page():
	if "role" in session and session["role"] == "student":
		studentcourses = student.get_students_ongoing_courses(session["user_id"])
		done = student.get_done(studentcourses[2], studentcourses[3])
		username = users.get_username(session["user_id"])
		return render_template("student.html", studentcourses=studentcourses[1], goals=studentcourses[2], studied=studentcourses[3], done=done, username=username)
	else:
		return render_template("notallowed.html")
	
@app.route("/study")
def study():
	if "role" in session and session["role"] == "student":
		courses = student.get_students_ongoing_courses(session["user_id"])
		return render_template("study.html", course_ids=courses[0], courses=courses[1])
	else:
		return render_template("notallowed.html")
	
@app.route("/studied", methods=["POST"])
def studied():
	student.update_studies(session["user_id"], request.form["course"], request.form["studied"])
	return redirect ("/study")
	
@app.route("/stats")
def stats():
	if "role" in session and session["role"] == "student":
		studentcourses = student.get_students_courses(session["user_id"])
		done = student.get_done(studentcourses[1], studentcourses[2])
		return render_template("stats.html", studentcourses=studentcourses[0], goals=studentcourses[1], studied=studentcourses[2], done=done, completed=studentcourses[3])
	else:
		return render_template("notallowed.html")
	
@app.route("/plan")
def plan():
	if "role" in session and session["role"] == "student":
		courses = student.get_courses_student_has_not_added(session["user_id"])
		studentcourses = student.get_students_ongoing_courses(session["user_id"])
		done = student.get_done(studentcourses[2], studentcourses[3])
		return render_template("plan.html", course_ids=courses[0], courses=courses[1], studentcourse_ids=studentcourses[0], studentcourses=studentcourses[1], goals=studentcourses[2], studied=studentcourses[3], done=done)
	else:
		return render_template("notallowed.html")
	
@app.route("/startcourse", methods=["POST"])
def start_course():
	student.start_course(request.form["course"], request.form["goal"], session["user_id"])
	return redirect("/plan")

@app.route("/coursedone", methods=["POST"])
def course_done():
	student.complete_course(request.form["course"], session["user_id"])
	return redirect("/plan")
	
@app.route("/changegoal", methods=["POST"])
def change_goal():
	student.change_plan(request.form["course"], request.form["goal"], session["user_id"])
	return redirect("/plan")
	
@app.route("/deletefromplan", methods=["POST"])
def delete_from_plan():
	student.delete_from_plan(request.form["course"], session["user_id"])
	return redirect("/plan")
	
@app.route("/teacher")
def teacher_page():
	if "role" in session and session["role"] == "teacher":
		results = teacher.get_ongoing_courses_table(session["user_id"])
		courses = results[0]
		student_counts = results[1]
		username = users.get_username(session["user_id"])
		return render_template("teacher.html", courses=courses, student_counts=student_counts, username=username)
	else:
		return render_template("notallowed.html")

@app.route("/grade")
def grade():
	if "role" in session and session["role"] == "teacher":
		courses = teacher.get_teachers_ongoing_courses(session["user_id"])
		return render_template("grade.html", courses=courses)
	else:
		return render_template("notallowed.html")
	
@app.route("/selectcourse", methods=["POST"])
def select_course():
	session["course"] = request.form["course"]
	return redirect("/gradecourse")
	
@app.route("/gradecourse")
def grade_course():
	if "role" in session and session["role"] == "teacher":
		students = teacher.get_students_from_course(session["course"])
		return render_template("grade_course.html", students=students)
	else:
		return render_template("notallowed.html")
	
@app.route("/addgrade", methods=["POST"])
def add_grade():
	teacher.add_grade(request.form["student"], session["course"], request.form["grade"])
	return redirect("/gradecourse")

@app.route("/graded", methods=["POST"])
def graded():
	if "role" in session and session["role"] == "teacher":
		del session["course"]
		return redirect("/grade")
	else:
		return render_template("notallowed.html")
	
@app.route("/teacherstats")
def teacher_stats():
	if "role" in session and session["role"] == "teacher":
		results = get_stats_table(session["user_id"])
		return render_template("teacher_stats.html", courses=results[0], student_counts=results[1], grade=results[2], studied=results[3])
	else:
		return render_template("notallowed.html")

	
@app.route("/courses")
def courses_page():
	if "user_id" in session:
		courses = teacher.get_courses()
		return render_template("courses.html", courses=courses)
	else:
		return render_template("notallowed.html")
	
@app.route("/courseadded", methods=["POST"])
def course_added():
	if "role" in session and session["role"] == "teacher":
		teacher.add_course(request.form["course"], session["user_id"])
	else:
		student.add_course(request.form["course"])
	return redirect("/courses")
