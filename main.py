from flask import Flask, render_template, request
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager(app=app)

from db import User, DB, simpleQuestion 


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
    if request.method == 'POST':
        name      = request.form.get('name')
        email     = request.form.get('email')
        password  = request.form.get('password')
        password2 = request.form.get('password2')
        checkbox  = request.form.get('teacher')

        if password == password2:
            User.create(username=name, email=email, password=password, teacher=checkbox)
            return render_template('signup.html', error=False)
        else:
            return render_template('signup.html', error=True)
    return render_template('signup.html', error=False)



@app.route('/test', methods=('GET', 'POST'))
def testen():
    return render_template('test.html', question=simpleQuestion.select().where(simpleQuestion.id == 1).get())

@app.route('/resultat', methods=('GET', 'POST'))
def resultatet():
    return render_template('resultat.html')

@app.route('/teacher_login', methods=('GET', 'POST'))
def teacher():
    return render_template('teacher_login.html')


# For hver gang der bliver kørt en request bliver denne funktion kørt først
@app.before_request
def before_request():
    DB.connect()

# For hver gang der bliver kørt en request bliver denne funktion kørt efter request'en et kørt
@app.after_request
def after_request(response):
    DB.close()
    return response


if __name__ == '__main__':
    app.run()
