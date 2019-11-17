from flask import Flask, flash, redirect, url_for, render_template, request, session, abort, render_template_string
import random
import sqlite3
from utilities import get_credentials, pluck_student_keys, pluck_quiz_keys, insert_student, insert_quiz, query_quiz_all, query_student_all, get_results, config_quiz_keys, config_student_keys, merge_tuples_to_dict, pluck_result_keys, insert_results, find_student_quizes, config_results_keys, find_quizes_with_students, config_anon_view_keys

app = Flask(__name__)
keys = get_credentials()
app.secret_key = keys['secret_key']
conn = sqlite3.connect('students.db', check_same_thread=False)

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/login')
def home():
    if not session.get('logged_in'):
        return render_template('login.html', cache_bust=random.random())
    else:
        session.pop('_flashes', None)
        return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def admin_login():
    print(request.form)
    if request.form['password'] == keys['password'] and request.form['username'] == keys['username']:
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

        return render_template('dashboard.html', student_values=student_values, quiz_values=quiz_values, cache_bust=random.random())
    else:
        flash('please login!')
        return redirect(url_for('home'))

@app.route('/student/<id>')
def get_students(id):
    if session.get('logged_in'):
        cursor = conn.cursor()
        result_query = find_student_quizes(id)
        details_results = get_results(cursor, result_query)
        details_values = merge_tuples_to_dict(config_results_keys(), details_results) if details_results else details_results

        return render_template('student.html', details_values=details_values, cache_bust=random.random())
    else:
        flash('please login!')
        return redirect(url_for('home'))

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

@app.route('/quiz/<id>/results/')
def get_quiz(id):
    cursor = conn.cursor()
    anon_query = find_quizes_with_students(id)

    anon_results = get_results(cursor, anon_query)
    anon_values = merge_tuples_to_dict(config_anon_view_keys(), anon_results) if anon_results else anon_results

    return render_template('quiz-detail.html', anon_values=anon_values, cache_bust=random.random())


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

        return render_template('results.html', student_values=student_values, quiz_values=quiz_values, cache_bust=random.random())
    else:
        return redirect(url_for('dashboard'))

@app.route('/results/add', methods=['POST'])
def add_quiz_result():
    form_values = request.form
    dict_form_values = dict(form_values)
    (student_id, quiz_id, grade) = pluck_result_keys(dict_form_values)

    cursor = conn.cursor()
    sql_script = insert_results(student_id, quiz_id, grade)
    cursor.executescript(sql_script)

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)