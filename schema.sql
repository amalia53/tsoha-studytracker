CREATE TABLE students (id SERIAL PRIMARY KEY,  username TEXT,  pw TEXT);
CREATE TABLE goals (id SERIAL PRIMARY KEY, student_id INTEGER, course_id INTEGER, goal INTEGER, studied INTEGER);
CREATE TABLE courses (id SERIAL PRIMARY KEY, course TEXT, teacher TEXT);
CREATE TABLE studentcourses (id SERIAL PRIMARY KEY, student_id INTEGER, course_id INTEGER);
