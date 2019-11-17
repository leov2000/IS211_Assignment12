import json

def get_credentials():
    with open('app_keys.json') as credentials:
        keys = json.load(credentials)
    
    return keys 

def pluck_student_keys(form_dict):
    first_name = form_dict.get('firstName', 'NA') 
    last_name = form_dict.get('lastName', 'NA')

    return (first_name, last_name)

def insert_student(first, last):
    sql_insert = f"""
    INSERT INTO students
    (first_name, last_name)
    VALUES('{first}', '{last}');
    """

    return sql_insert

def pluck_quiz_keys(form_dict):
    subject_name = form_dict['subjectName']
    question_num = form_dict['questionNum']
    quiz_date = form_dict['quizDate']

    return (subject_name, question_num, quiz_date)

def insert_quiz(subject, num, quiz_date):
    sql_insert = f"""
    INSERT INTO quizes
    (subject_name, questions, quiz_date)
    VALUES('{subject}', '{num}', '{quiz_date}');
    """
    return sql_insert

def query_student_all():
    sql_query = "SELECT * FROM students;"

    return sql_query

def query_quiz_all():
    sql_query = "SELECT * FROM quizes;"

    return sql_query

def get_results(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()

    return result 

def config_student_keys():
    key_tuple = ('student_id', 'last_name', 'first_name')

    return key_tuple

def config_quiz_keys():
    quiz_tuple = ('quiz_id', 'subject', 'quiz_num', 'quiz_date')

    return quiz_tuple

def config_results_keys():
    results_tuple = ('first_name', 'last_name', 'subject', 'quiz_id', 'quiz_date', 'score')

    return results_tuple

def config_anon_view_keys():
    results_tuple = ('person_id', 'subject', 'quiz_id', 'quiz_date', 'score')

    return results_tuple

def merge_tuples_to_dict(key_tup, val_tup_list):
    result_list = [dict(zip(key_tup, val_tup)) for val_tup in val_tup_list]

    return result_list

def pluck_result_keys(form_dict):
    student_id = int(form_dict['student'])
    quiz_id = int(form_dict['quiz'])
    grade = int(form_dict['grade'])

    return (student_id, quiz_id, grade)

def insert_results(student, quiz, grade):
    sql_insert = f"""
    INSERT INTO results
    (student_id, quiz_id, grade)
    VALUES('{student}', '{quiz}', '{grade}');
    """
    return sql_insert

def find_student_quizes(id):
    sql_query = f"""
    SELECT 
    students.first_name AS 'PersonFirst',
    students.last_name AS 'PersonLast', 
	quizes.subject_name AS 'quizSubject',
    quizes.quiz_id AS 'quizId',
    quizes.quiz_date as 'quizDate',
    results.grade AS 'resultsScore'
    FROM students
	JOIN results ON students.student_id = results.student_id
    JOIN quizes ON results.quiz_id = quizes.quiz_id
    WHERE students.student_id IS {id};
    """
    return sql_query

def find_quizes_with_students(id):
    sql_query = f"""
    SELECT 
    students.student_id AS 'personId',
	quizes.subject_name AS 'quizSubject',
    quizes.quiz_id AS 'quizId',
    quizes.quiz_date as 'quizDate',
    results.grade AS 'resultsScore'
    FROM students
	JOIN results ON students.student_id = results.student_id
    JOIN quizes ON results.quiz_id = quizes.quiz_id
    WHERE quizes.quiz_id IS {id};
    """
    return sql_query