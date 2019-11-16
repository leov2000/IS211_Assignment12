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

def student_keys():
    # [(1, 'black', 'jack')]
    key_tuple = ('student_id', 'last_name', 'first_name')

    return key_tuple

def quiz_keys():
    # [(1, 'Rock', '100', '2019-11-05')]
    quiz_tuple = ('quiz_id', 'subject', 'quiz_num', 'quiz_date')

    return quiz_tuple

def merge_tuples_to_dict(key_tup, val_tup_list):
    result_list = [dict(zip(key_tup, val_tup)) for val_tup in val_tup_list]

    return result_list




