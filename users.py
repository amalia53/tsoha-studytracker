from db import db
from werkzeug.security import check_password_hash, generate_password_hash

import teacher

def login(username, pw):
    sql = "SELECT pw, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchall()
#    sql = "SELECT role FROM users WHERE username=:username"
#    result = db.session.execute(sql, {"username":username})
#    role = result.fetchone() 
    if user == None:
        return "invalid_username"
    else:
        return check_pw(user[0], pw, user[1])
        
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
        	user_id = get_user_id(username)[0]
        	teacher.add_teacher(name, user_id)
        	return "ok"
        else:
        	return reg
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
