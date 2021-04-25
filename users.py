from db import db
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, pw):
    sql = "SELECT pw FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    user_pw = user[0]
    sql = "SELECT role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone() 
    role = user[0]
    if user_pw == None:
        return "invalid_username"
    else: 		
        return check_pw(user_pw, pw, role)
        
def check_pw(user_pw, pw, role):
    hash_pw = user_pw
    if check_password_hash(hash_pw, pw):
    	return role
    else:
        return "invalid_pw"

def student_reg(username, pw, verification):
    return register(username, pw, verification, "student")
        
def teacher_reg(username, name, pw, verification, code):
    if code == "4278":
        reg = register(username, pw, verification, "teacher")
        if reg == "ok":
        	user_id = get_user_id(username)
        	teacher.add_teacher(name, user_id)
    else:
        return "not_authenticated" 

def register(username, pw, verification, role):
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        if pw == verification:
            hash_pw = generate_password_hash(pw)
            sql = "INSERT INTO users (username, pw, role) VALUES (:username, :pw, :role)"
            db.session.execute(sql, {"username":username, "pw":hash_pw, "role":role})
            db.session.commit()
            return "ok"
        else:
            return "no_match"
    else:
        return "user_found"
        
def get_user_id(username):
	sql = "SELECT id FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone()
    
def get_user_role(username):
	sql = "SELECT role FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	return result.fetchone()
	
def is_teacher(username):
	return get_user_role == "teacher"
