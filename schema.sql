-- Check and see if the artists table already exists, if it does, drop it
DROP TABLE IF EXISTS students;

-- Check and see if the albums table already exists, if it does, drop it
DROP TABLE IF EXISTS quizes;

-- Check and see if the songs table already exists, if it does, drop it
DROP TABLE IF EXISTS results;

-- Create artist table
CREATE TABLE students (
    artist_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    last_name TEXT,
    first_name TEXT
);

-- Create albums table
CREATE TABLE quizes (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    subject_name TEXT,
    questions TEXT,
    quiz_date DATE
);

-- Create song table
CREATE TABLE results (
    results_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    student_id INT NOT NULL,
    quiz_id INT NOT NULL
);
