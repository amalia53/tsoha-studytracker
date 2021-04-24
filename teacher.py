from db import db

def get_teacher_name(username):
	sql = "SELECT name FROM teachers WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone()
	
def get_teacher_id(name):
	sql = "SELECT id FROM teachers WHERE name=:name"
	result = db.session.execute(sql, {"name":name})
	return result.fetchone()
