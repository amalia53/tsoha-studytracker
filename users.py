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
			

