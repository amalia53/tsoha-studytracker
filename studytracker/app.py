from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///amalia"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
	result = db.session.execute("SELECT COUNT(*) FROM students")
	count = result.fetchone()[0]
	return render_template("index.html", count = count)

@app.route("/login")
def login():
        return render_template("login.html")

@app.route("/loggedin", methods=["POST"])
def logged_in():
	username = request.form["username"]
	pw = request.form["password"]
	sql = "SELECT pw FROM students WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone() 
	if user == None:
		return render_template("invalid.html", invalid = "käyttäjätunnus")
	else:
		hash_pw = user[0]
		if check_password_hash(hash_pw, pw):
			session["username"] = username
			return render_template("logged_in.html")
		else:
			return render_template("invalid.html", invalid = "salasana")

@app.route("/stureg")
def stu_reg():
        return render_template("studentReg.html")

@app.route("/teachreg")
def teach_reg():
        return render_template("teacherReg.html")

@app.route("/welcome", methods=["POST"])
def welcome():
	username = request.form["username"]
	pw = request.form["password"]
	hash_pw = generate_password_hash(pw)
	sql = "INSERT INTO students (username, pw) VALUES (:username, :pw)"
	db.session.execute(sql, {"username":username, "pw":hash_pw})
	db.session.commit()
	return render_template("welcome.html", username = username)

@app.route("/student")
def student():
        return render_template("student.html")

@app.route("/courses")
def courses():
	result = db.session.execute("SELECT course FROM courses")
	courses = result.fetchall()
	return render_template("courses.html", courses = courses)

@app.route("/addcourse")
def add_course():
	return render_template("add_course.html")
	
@app.route("/courseadded", methods=["POST"])
def course_added():
	course = request.form["course"]
	teacher = request.form["teacher"]
	sql = "INSERT INTO courses (course, teacher) VALUES (:course, :teacher)"
	db.session.execute(sql, {"course":course, "teacher":teacher})
	db.session.commit()
	return render_template("course_added.html")
