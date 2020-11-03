from flask import Flask, render_template, request
from db import Student, DB

app = Flask(__name__)

@app.route('/', methods=('GET',))
def home():
    return render_template('hovedmenu.html')


@app.route('/layout', methods=('GET',))
def layout():
    return render_template('layout.html')

@app.route('/student_login', methods=('GET', 'POST'))
def student():
    return render_template('student_login.html')

@app.route('/startside', methods=('GET', 'POST'))
def start():
    return render_template('startside.html')

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    return render_template('signup.html')

@app.route('/test', methods=('GET', 'POST'))
def testen():
    return render_template('test.html', students=Student.select())

@app.route('/resultat', methods=('GET', 'POST'))
def resultatet():
    return render_template('resultat.html')

@app.route('/teacher_login', methods=('GET', 'POST'))
def teacher():
    name = request.form['name']
    print(name)
    return render_template('teacher_login.html', namelol=name)


# For hver gang der bliver kørt en request bliver denne funktion kørt først
@app.before_request
def before_request():
    DB.connect()

# For hver gang der bliver kørt en request bliver denne funktion kørt efter request'en
@app.after_request
def after_request(response):
    DB.close()
    return response


if __name__ == '__main__':
    app.run()
