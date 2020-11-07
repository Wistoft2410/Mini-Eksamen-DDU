from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user

app = Flask(__name__)

# Man skal have en "secret_key" for at kryptere bruger browser sessionen!
app.secret_key = '387r3q897thghds0-'

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
    if request.method == 'POST':
        email     = request.form.get('email')
        password  = request.form.get('password')
        user = User.get_or_none(User.email == email.lower())
        if not user:
            # Det her kører hvis brugeren ikke har angivet den rigtige email 
            return render_template('student_login.html', error_msg="Denne email findes ikke!")
        else:
            if user.password == password:
                # Det her kører hvis brugeren HAR angivet det rigtige password 
                login_user(user)
                return redirect(url_for('start'))
            else:
                # Det her kører hvis brugeren ikke har angivet det rigtige password 
                return render_template('student_login.html', error_msg="Denne adgangskode passer ikke!")

    # Det her kører hvis brugeren bare har lavet en "GET" request til denne rute
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
            User.create(username=name, email=email, password=password, teacher=(True if checkbox else False))
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
