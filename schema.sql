CREATE TABLE students (id SERIAL PRIMARY KEY,  username TEXT UNIQUE,  pw TEXT);
CREATE TABLE goals (id SERIAL PRIMARY KEY, student_id INTEGER REFERENCES students (id), course_id INTEGER REFERENCES courses (id), goal INTEGER, studied INTEGER);
CREATE TABLE courses (id SERIAL PRIMARY KEY, course TEXT, teacher TEXT);
CREATE TABLE studentcourses (id SERIAL PRIMARY KEY, student_id INTEGER REFERENCES students (id), course_id INTEGER REFERENCES courses (id), ongoing BOOLEAN DEAFULT TRUE, visible BOOLEAN DEFAULT TRUE	);
