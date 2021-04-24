from db import db

def get_teacher_name(username):
	sql = "SELECT name FROM teachers WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone()

