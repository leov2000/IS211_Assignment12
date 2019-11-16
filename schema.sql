-- Check and see if the students table already exists, if it does, drop it
DROP TABLE IF EXISTS students;

-- Check and see if the quizes table already exists, if it does, drop it
DROP TABLE IF EXISTS quizes;

-- Check and see if the results table already exists, if it does, drop it
DROP TABLE IF EXISTS results;

-- Create students table
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    last_name TEXT,
    first_name TEXT
);

-- Create albums quizes
CREATE TABLE quizes (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    subject_name TEXT,
    questions TEXT,
    quiz_date DATE
);

-- Create song results
CREATE TABLE results (
    results_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    student_id INT NOT NULL,
    quiz_id INT NOT NULL
);
