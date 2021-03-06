from db import db

import users

def start_course(course_id, goal, user_id):
    sql = "INSERT INTO goals (user_id, course_id, goal, studied) VALUES (:user_id, :course_id, :goal, :studied)"
    db.session.execute(sql, {"user_id":user_id, "course_id":course_id, "goal":goal, "studied":0})
    db.session.commit()
    
def complete_course(course_id, user_id):
    sql = "UPDATE goals SET completed = NOT completed WHERE user_id=:user_id AND course_id=:course_id"
    db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    db.session.commit()
    
def change_plan(course_id, goal, user_id):
    sql = "UPDATE goals SET goal=:goal WHERE user_id=:user_id AND course_id=:course_id"
    db.session.execute(sql, {"goal":goal, "user_id":user_id, "course_id":course_id})
    db.session.commit()
    
def delete_from_plan(course_id, user_id):
    sql = "UPDATE goals SET deleted = NOT deleted WHERE user_id=:user_id AND course_id=:course_id"
    db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    db.session.commit()

def add_to_arrays_4(results):
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    for result in results:
        result1.append(result[0])
        result2.append(result[1])
        result3.append(result[2])
        result4.append(result[3])
    return result1, result2, result3, result4
    
def add_to_arrays_2(results):
    result1 = []
    result2 = []
    for result in results:
        result1.append(result[0])
        result2.append(result[1])
    return result1, result2

def get_students_ongoing_courses(user_id):
    sql = "SELECT c.id, c.course, g.goal, g.studied FROM goals g JOIN courses c ON g.course_id = c.id WHERE g.user_id=:user_id AND NOT completed AND NOT deleted ORDER BY course ASC"
    results = db.session.execute(sql, {"user_id":user_id})
    return add_to_arrays_4(results.fetchall())
    
def get_students_courses(user_id):
    sql = "SELECT course, goal, studied, completed FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT deleted ORDER BY courses.course ASC"
    results = db.session.execute(sql, {"user_id":user_id})
    return add_to_arrays_4(results.fetchall())

def get_courses_student_has_not_added(user_id):
    sql = "SELECT id, course FROM courses WHERE NOT id IN (SELECT course_id FROM goals WHERE user_id=:user_id AND NOT deleted) ORDER BY course ASC"
    results = db.session.execute(sql, {"user_id":user_id})
    return add_to_arrays_2(results.fetchall())

def get_done(goals, studied):
    done = []
    for i in range(len(goals)):
        prosent = (studied[i] / goals[i]) * 100
        prosent = int(prosent)
        done.append(prosent)
    return done

def get_completed(user_id):
    sql = "SELECT completed FROM goals JOIN courses ON goals.course_id = courses.id WHERE goals.user_id=:user_id AND NOT deleted ORDER BY courses.course ASC"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall() 

def update_studies(user_id, course_id, studied):
    studied = int(studied)
    studied_pre = get_previous_studies(user_id, course_id)
    studied += studied_pre
    sql = "UPDATE goals SET studied=:studied WHERE user_id=:user_id AND course_id=:course_id"
    result = db.session.execute(sql, {"studied":studied, "course_id":course_id, "user_id":user_id})
    db.session.commit()

def get_previous_studies(user_id, course_id):
    sql = "SELECT studied FROM goals WHERE user_id=:user_id AND course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    previous_studies = result.fetchone()
    return previous_studies[0]

def add_course(course):
	sql = "INSERT INTO courses (course) VALUES (:course)"
	db.session.execute(sql, {"course":course})
	db.session.commit()
