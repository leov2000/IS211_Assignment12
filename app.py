from flask import Flask, flash, redirect, render_template, request, session, abort, render_template_string
import random
from utilities import get_credentials

app = Flask(__name__)
keys = get_credentials()
app.secret_key = keys['secret_key']

@app.route('/login')
def home():
    if not session.get('logged_in'):
        return render_template('login.html', cache_bust=random.random())
    else:
        return render_template_string("Hi")

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
    """
    shows a listing of students i the class and a listing of quizzes
    in the class, in two separate tables. Each row of the student table should
    list the ID, first and last name of all student enrolled in this class.
    Each row of the quiz table should list the
    ID, subject, number of questions and the quiz date.
    """

@app.route('/student<id>')
def get_student():
    """
    where id is the ID of the student. This route should display all quiz results for
    the student with the given ID. If there are no results, you shouldoutput “No Results’ to the page;
    otherwise, an HTML table should be displayed showing the Quiz ID and theScore on the quiz.
    """

@app.route('/student/add', methods=['POST'])
def add_student():
    """
    Display an HTML form capable of adding a new student (HINT: there should be no
    reason to have an ID field in this form, as that should be taken care of by the database)
    Accepts the HTML form and attempts to add a new student to the database with the given form
    information. Upon success, redirect back to the ‘/dashboard’ route. If there is a failure,
    return the same HTML form with an error message
    """

@app.route('/quiz/add', methods=['POST'])
def add_quiz():
    """"
    We also need to be able to add quizzes. Repeat the prior step, but for a quiz instead of a student. This route
    should be located at ‘/quiz/add’. Think about how best to represent a date using HTML forms, as you have a
    few options.
    """

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
    app.run()
