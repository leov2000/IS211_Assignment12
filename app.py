from flask import Flask, flash, redirect, url_for, render_template, request, session, abort, render_template_string
import random
import sqlite3
from utilities import get_credentials, pluck_student_keys, pluck_quiz_keys, insert_student, insert_quiz, query_quiz_all, query_student_all, get_results, config_quiz_keys, config_student_keys, merge_tuples_to_dict

app = Flask(__name__)
keys = get_credentials()
app.secret_key = keys['secret_key']
conn = sqlite3.connect('students.db', check_same_thread=False)

@app.route('/login')
def home():
    if not session.get('logged_in'):
        return render_template('login.html', cache_bust=random.random())
    else:
        session.pop('_flashes', None)
        return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def admin_login():
    if request.form['password'] == keys['password'] and keys['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')

    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.pop('_flashes', None)

    return home()

@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        cursor = conn.cursor()
        students_query = query_student_all()
        quiz_query = query_quiz_all()
        
        student_results = get_results(cursor, students_query)
        quiz_results = get_results(cursor, quiz_query)

        student_values = merge_tuples_to_dict(config_student_keys(), student_results) if student_results else student_results
        quiz_values = merge_tuples_to_dict(config_quiz_keys(), quiz_results) if quiz_results else quiz_results

        print(student_values)
        print(quiz_values)

        return render_template('dashboard.html', student_values=student_values, quiz_values=quiz_values, cache_bust=random.random())
    else:
        flash('please login!')
        return redirect(url_for('home'))

@app.route('/student/<id>')
def get_students(id):
    if session.get('logged_in'):
        return render_template('student.html', cache_bust=random.random())
    else:
        flash('please login!')
        return redirect(url_for('home'))

    """
    where id is the ID of the student. This route should display all quiz results for
    the student with the given ID. If there are no results, you shouldoutput “No Results’ to the page;
    otherwise, an HTML table should be displayed showing the Quiz ID and theScore on the quiz.
    """

@app.route('/student/add', methods=['POST'])
def add_student():
    if session.get('logged_in') and request.form:
        form_values = request.form
        dict_form_values = dict(form_values)
        (first, last) = pluck_student_keys(dict_form_values)

        cursor = conn.cursor()
        sql_script = insert_student(first, last)
        cursor.executescript(sql_script)

        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/quiz/add', methods=['POST'])
def add_quiz():
    if session.get('logged_in') and request.form:
        form_values = request.form
        dict_form_values = dict(form_values)
        (subject, num, quiz_date) = pluck_quiz_keys(dict_form_values)

        cursor = conn.cursor()
        sql_script = insert_quiz(subject, num, quiz_date)
        cursor.executescript(sql_script)

        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/quiz/<id>')
def get_quiz(id):
    if session.get('logged_in'):
        return render_template('student.html', cache_bust=random.random())
    else:
        flash('please login!')
        return redirect(url_for('home'))

@app.route('/results/add')
def results_page():
    if session.get('logged_in'):
        cursor = conn.cursor()
        students_query = query_student_all()
        quiz_query = query_quiz_all()
        
        student_results = get_results(cursor, students_query)
        quiz_results = get_results(cursor, quiz_query)

        student_values = merge_tuples_to_dict(config_student_keys(), student_results) if student_results else student_results
        quiz_values = merge_tuples_to_dict(config_quiz_keys(), quiz_results) if quiz_results else quiz_results

        print(student_values)
        print(quiz_values)
        return render_template('results.html', student_values=student_values, quiz_values=quiz_values, cache_bust=random.random())
    else:
        return redirect(url_for('dashboard'))

@app.route('/results/add', methods=['POST'])
def add_quiz_result():
    """
    This route should display an HTML form capable of adding a quiz result. Since a result
    links a student and a quiz together, we need to be able to select a student and to select a quiz.
    Implement both of these as a dropdown menu, which lists the possible students and quizzes to choose from.
    Don’t forget to add an input field for the grade as well. If successful, this should redirect to the dashboard;
    if there is a failure, show the HTML form again with an error message.
    """

# @app.route('/results')
# def view_results():
#     """
#     Allow a non­logged in user to see quiz results but only in a anonymized way
#     (i.e. show a student ID instead of the user name)
#     """

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)