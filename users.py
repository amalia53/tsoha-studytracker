from db import db
from werkzeug.security import check_password_hash, generate_password_hash

import teacher

def login(username, pw):
    sql = "SELECT pw, role, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    results = result.fetchall()
    if not results:
        return "invalid", "username"
    else:
        return check_pw(results, pw)
        
def check_pw(results, pw):
    hash_pw = results[0][0]
    user_role = results[0][1]
    user_id = results[0][2]
    if check_password_hash(hash_pw, pw):
    	return user_id, user_role
    else:
        return "invalid", "password"

def student_reg(username, pw, verification):
    return register(username, pw, verification, "student")
        
def teacher_reg(username, name, pw, verification, code):
    if code == "4278":
        reg = register(username, pw, verification, "teacher")
        if reg == "ok":
            user_id = get_user_id(username)
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
    if check_input(username, pw) == "ok":  	
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
    else:
        return check_input(username, pw)
    	
def check_input(username, pw):
    if len(username) < 5:
	return "username_too_short"
    elif len(pw) < 8:
	return "pw_too_short"
    else:
	return "ok"
        
def get_user_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()
    return user_id[0]
    
def get_username(user_id):
    sql = "SELECT username FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    username = result.fetchone()
    return username[0]
    
