from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

def login(username, pw):
	sql = "SELECT pw FROM students WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	student = result.fetchone() 
	if student == None:
		teacher = check_user(username, "teachers")
		if teacher == None:
			return "invalid_username"
		else:
			if check_pw(teacher, pw) == "ok":
				return "teacher"
			return isPwOk
	else:
		return check_pw(user, pw)

def check_user(username, table):
	sql = "SELECT pw FROM " + table + " WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone() 
		
def check_pw(user, pw):
	hash_pw = user[0]
	if check_password_hash(hash_pw, pw):
		return "ok"
	else:
		return "invalid_pw"

def student_reg(username, name, pw, verification):
	return register("students", username, name, pw, verification)
		
def teacher_reg(username, name, pw, verification, code):
	if code == "4278":
		return register("teachers", username, name, pw, verification)
	else:
		return "not_authenticated" 

def register(table, username, name, pw, verification):
	sql = "SELECT username FROM students WHERE username=:username UNION SELECT username FROM teachers WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if user == None:
		if pw == verification:
			hash_pw = generate_password_hash(pw)
			sql = "INSERT INTO " + table +  " (username, name, pw) VALUES (:username, :name, :pw)"
			db.session.execute(sql, {"username":username, "name":name, "pw":hash_pw})
			db.session.commit()
			return "ok"
		else:
			return "no_match"
	else:
		return "user_found"
