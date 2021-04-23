from db import db

def login(username, pw):
	sql = "SELECT pw FROM students WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone() 
	if user == None:
		return "invalid_username"
	else:
		hash_pw = user[0]
		if check_password_hash(hash_pw, pw):
			session["username"] = username
			return "ok"
		else:
			return "invalid_pw"
			
def get_session():
	return session["username"]

def student_reg(usename, pw, verication):
	sql = "SELECT username FROM students WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if user == None:
		if pw == verification:
			hash_pw = generate_password_hash(pw)
			sql = "INSERT INTO students (username, pw) VALUES (:username, :pw)"
			db.session.execute(sql, {"username":username, "pw":hash_pw})
			db.session.commit()
			return "ok"
		else:
			return "no_match"
	else:
		return "user_found"
