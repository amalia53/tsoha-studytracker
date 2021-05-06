from db import db

import users

def start_course(course, goal, username):
    course_id = get_course_id(course)
    user_id = users.get_user_id(username)
    sql = "INSERT INTO goals (user_id, course_id, goal, studied) VALUES (:user_id, :course_id, :goal, :studied)"
    db.session.execute(sql, {"user_id":user_id[0], "course_id":course_id, "goal":goal, "studied":0})
    db.session.commit()

def complete_course(course, username):
    course_id = get_course_id(course)
    user_id = users.get_user_id(username)
    sql = "UPDATE goals SET completed = NOT completed WHERE user_id=:user_id AND course_id=:course_id"
    db.session.execute(sql, {"user_id":user_id[0], "course_id":course_id})
    db.session.commit()
    
def change_plan(course, goal, username):
    course_id = get_course_id(course)
    user_id = users.get_user_id(username)
    sql = "UPDATE goals SET goal=:goal WHERE user_id=:user_id AND course_id=:course_id"
    db.session.execute(sql, {"goal":goal, "user_id":user_id[0], "course_id":course_id})
    db.session.commit()
    
def delete_from_plan(course, username):
    course_id = get_course_id(course)
    user_id = users.get_user_id(username)
    sql = "UPDATE goals SET deleted = NOT deleted WHERE user_id=:user_id AND course_id=:course_id"
    db.session.execute(sql, {"user_id":user_id[0], "course_id":course_id})
    db.session.commit()
    
def get_course_id(course):
    sql = "SELECT id FROM courses WHERE course=:course"
    result = db.session.execute(sql, {"course":course})
    return result.fetchone()
    
def get_students_ongoing_courses(username):
    user_id = users.get_user_id(username)
    sql = "SELECT course FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT completed AND NOT deleted"
    result = db.session.execute(sql, {"user_id":user_id[0]})
    studentcourses = result.fetchall()
    return studentcourses
    
def get_students_courses(username):
    user_id = users.get_user_id(username)
    sql = "SELECT course FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT deleted"
    result = db.session.execute(sql, {"user_id":user_id[0]})
    studentcourses = result.fetchall()
    return studentcourses

def get_courses_student_has_not_added(username):
    user_id = users.get_user_id(username)
    sql = "SELECT course FROM courses WHERE NOT id IN (SELECT course_id FROM goals WHERE user_id=:user_id AND NOT deleted)"
    result = db.session.execute(sql, {"user_id":user_id[0]})
    return result.fetchall()

def get_students_goals(username):
    user_id = users.get_user_id(username)
    sql = "SELECT goal FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT deleted"
    result = db.session.execute(sql, {"user_id":user_id[0]})
    return result.fetchall()
    
def get_students_ongoing_goals(username):
    user_id = users.get_user_id(username)
    sql = "SELECT goal FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT completed AND NOT deleted"
    result = db.session.execute(sql, {"user_id":user_id[0]})
    return result.fetchall()
    
def get_students_ongoing_studies(username):
    user_id = users.get_user_id(username)
    sql = "SELECT studied FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT completed AND NOT deleted"
    result = db.session.execute(sql, {"user_id":user_id[0]})
    return result.fetchall()     
    
def get_students_studies(username):
    user_id = users.get_user_id(username)
    sql = "SELECT studied FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT deleted"
    result = db.session.execute(sql, {"user_id":user_id[0]})
    return result.fetchall() 

def get_done(studentcourses, goals, studied):
    done = []
    rng = len(studentcourses)
    for i in range(rng):
        prosent = (studied[i][0] / goals[i][0]) * 100
        prosent = int(prosent)
        done.append(prosent)
    return done

def get_completed(username):
    user_id = users.get_user_id(username)
    sql = "SELECT completed FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT deleted"
    result = db.session.execute(sql, {"user_id":user_id[0]})
    return result.fetchall() 

def update_studies(username, course, studied):
    user_id = users.get_user_id(username)
    course_id = get_course_id(course)
    studied = int(studied)
    studied_pre = get_previous_studies(username, course, user_id, course_id)[0]    
    studied += studied_pre
    sql = "UPDATE goals SET studied=:studied WHERE user_id=:user_id AND course_id=:course_id"
    result = db.session.execute(sql, {"studied":studied, "course_id":course_id, "user_id":user_id[0]})
    db.session.commit()

def get_previous_studies(username, course, user_id, course_id):
    sql = "SELECT studied FROM goals WHERE user_id=:user_id AND course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id[0], "user_id":user_id[0]})
    return result.fetchone()

def add_course(course):
	sql = "INSERT INTO courses (course) VALUES (:course)"
	db.session.execute(sql, {"course":course})
	db.session.commit()
