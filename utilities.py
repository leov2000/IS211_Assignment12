import json

def get_credentials():
    """
    A utility function used to get the secret keys form the app.keys.json file
    Parmeters: None
    Returns: A dictionary with the credential values.
    """
    with open('app_keys.json') as credentials:
        keys = json.load(credentials)
    
    return keys 

def pluck_student_keys(form_dict):
    """
    A utility getter function used to pluck keys from a form dict.
    Parameters: form_dict(dict[str])
    Returns a tuple with the plucked values.
    """
    first_name = form_dict.get('firstName', 'NA') 
    last_name = form_dict.get('lastName', 'NA')

    return (first_name, last_name)

def insert_student(first, last):
    """
    A utility function that interpolates the student fields into a sql_insert string.

    Parameters:
        first(str)
        none(str)

    Returns: A sql insert string.
    """
    sql_insert = f"""
    INSERT INTO students
    (first_name, last_name)
    VALUES('{first}', '{last}');
    """

    return sql_insert

def pluck_quiz_keys(form_dict):
    """
    A utility getter function used to pluck keys from a form dict.
    Parameters: form_dict(dict[str])
    Returns a tuple with the plucked values.
    """
    subject_name = form_dict['subjectName']
    question_num = form_dict['questionNum']
    quiz_date = form_dict['quizDate']

    return (subject_name, question_num, quiz_date)

def insert_quiz(subject, num, quiz_date):
    """
    A utility function that interpolates the quiz fields into a sql_insert string.

    Parameters:
        subject(str)
        num(str)
        quiz_date(str)

    Returns: A sql insert string.
    """
    sql_insert = f"""
    INSERT INTO quizes
    (subject_name, questions, quiz_date)
    VALUES('{subject}', '{num}', '{quiz_date}');
    """
    return sql_insert

def query_student_all():
    """
    A query string that queries the student table
    Parameters: None
    Returns: A sql query string
    """
    sql_query = "SELECT * FROM students;"

    return sql_query

def query_quiz_all():
    """
    A query string that queries the quizes table
    Parameters: None
    Returns: A sql query string
    """
    sql_query = "SELECT * FROM quizes;"

    return sql_query

def get_results(cursor, query):
    """
    A sqlite utility function that executes a query and
    gets the results from the sqlite cursor object.

    Parameters:
        cursor(<cursor object>)
        query(str)
    
    Returns: A list of tuple values.
    """
    cursor.execute(query)
    result = cursor.fetchall()

    return result 

def config_student_keys():
    """
    A function that returns a tuple config used for generating dictionary keys
    Parameters: None
    Returns: tuple of strings.
    """
    key_tuple = ('student_id', 'last_name', 'first_name')

    return key_tuple

def config_quiz_keys():
    """
    A function that returns a tuple config used for generating dictionary keys
    Parameters: None
    Returns: tuple of strings.
    """
    quiz_tuple = ('quiz_id', 'subject', 'quiz_num', 'quiz_date')

    return quiz_tuple

def config_results_keys():
    """
    A function that returns a tuple config used for generating dictionary keys
    Parameters: None
    Returns: tuple of strings.
    """
    results_tuple = ('first_name', 'last_name', 'subject', 'quiz_id', 'quiz_date', 'score')

    return results_tuple

def config_anon_view_keys():
    """
    A function that returns a tuple config used for generating dictionary keys
    Parameters: None
    Returns: tuple of strings.
    """
    results_tuple = ('person_id', 'subject', 'quiz_id', 'quiz_date', 'score')

    return results_tuple

def merge_tuples_to_dict(key_tup, val_tup_list):
    """
    A utility function used to merge two tuples into a list of dictionaries
    for the view portion.

    Parameters: 
        key_tup(tup(str))
        val_tup_list(list(tup(str)))

    Returns a list of dictionaries
    """
    result_list = [dict(zip(key_tup, val_tup)) for val_tup in val_tup_list]

    return result_list

def pluck_result_keys(form_dict):
    """
    A utility getter function used to pluck keys from a form dict.
    Parameters: form_dict(dict[str])
    Returns a tuple with the plucked values.
    """
    student_id = int(form_dict['student'])
    quiz_id = int(form_dict['quiz'])
    grade = int(form_dict['grade'])

    return (student_id, quiz_id, grade)

def insert_results(student, quiz, grade):
    """
    A utility function that interpolates the student fields into a sql_insert string.

    Parameters:
        student(str)
        quiz(str)
        grade(str)

    Returns: A sql insert string.
    """
    sql_insert = f"""
    INSERT INTO results
    (student_id, quiz_id, grade)
    VALUES('{student}', '{quiz}', '{grade}');
    """
    return sql_insert

def find_student_quizes(id):
    """
    A query string that queries the student table and joins results and quizes on the student_id
    with a particular id value.

    Parameters: id(str)

    Returns: A sql query string
    """
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
    """
    A query string that queries the student table and joins results and quizes on the quiz_id 
    with a particular id value.

    Parameters: id(str)
    
    Returns: A sql query string
    """
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