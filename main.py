from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user

app = Flask(__name__)

# Man skal have en "secret_key" for at kryptere bruger browser sessionen!
app.secret_key = '387r3q897thghds0-'

login_manager = LoginManager(app=app)
login_manager.session_protection = 'strong'


from db import User, DB, simpleQuestion, userQuestionRel


@app.route('/', methods=('GET',))
def home():
    return render_template('hovedmenu.html')


@app.route('/student_login', methods=('GET', 'POST'))
def student_login():
    if request.method == 'POST':
        email     = request.form.get('email')
        password  = request.form.get('password')

        # Tjek om brugeren ikke er en lærer og om der er en bruger der har den email brugeren har angivet
        # Hvis du gerne vil vide mere om hvad tegnene betyder såsom "~" og "&" så følg følgende link:
        # http://docs.peewee-orm.com/en/latest/peewee/query_operators.html
        user = User.get_or_none(~(User.teacher) & (User.email == email.lower()))
        if not user:
            # Det her kører hvis brugeren ikke har angivet den rigtige email 
            return render_template('student_login.html', error_msg="Denne email findes ikke i elev databasen!")
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


@app.route('/teacher_login', methods=('GET', 'POST'))
def teacher_login():
    if request.method == 'POST':
        email     = request.form.get('email')
        password  = request.form.get('password')

        # Tjek om brugeren ikke er en lærer og om der er en bruger der har den email brugeren har angivet
        # Hvis du gerne vil vide mere om hvad tegnene betyder såsom "~" og "&" så følg følgende link:
        # http://docs.peewee-orm.com/en/latest/peewee/query_operators.html
        user = User.get_or_none((User.teacher) & (User.email == email.lower()))
        if not user:
            # Det her kører hvis brugeren ikke har angivet den rigtige email 
            return render_template('student_login.html', error_msg="Denne email findes ikke i elev databasen!")
        else:
            if user.password == password:
                # Det her kører hvis brugeren HAR angivet det rigtige password 
                login_user(user)
                return redirect(url_for('start'))
            else:
                # Det her kører hvis brugeren ikke har angivet det rigtige password 
                return render_template('student_login.html', error_msg="Denne adgangskode passer ikke!")

    # Det her kører hvis brugeren bare har lavet en "GET" request til denne rute
    return render_template('teacher_login.html')


@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        name      = request.form.get('name')
        email     = request.form.get('email')
        password  = request.form.get('password')
        password2 = request.form.get('password2')
        checkbox  = request.form.get('teacher')

        if User.select().where(User.email == email).exists():
            return render_template('signup.html', error=False, error2=True)

        if password == password2:
            user = User.create(username=name, email=email, password=password, teacher=(True if checkbox else False))
            login_user(user)
            return redirect(url_for('start'))
        else:
            return render_template('signup.html', error=True)
    return render_template('signup.html', error=False)


@app.route('/startside', methods=('GET', 'POST'))
@login_required
def start():
    return render_template('startside.html')


@app.route('/test', methods=('GET', 'POST'))
@login_required
def testen():
    return render_template('test.html', question=simpleQuestion.get_or_none(simpleQuestion.id == 1))


@app.route('/resultat', methods=('POST',))
@login_required
def resultatet():
    answer = request.form.get('answer')
    ID = request.form.get('id')
    question = simpleQuestion.get_or_none(ID)

    answeredCorrectly = False

    if question:
        if question.yesOrNo:
            if question.answer1 == answer:
                answeredCorrectly = True

        elif question.answer2 == answer:
            answeredCorrectly = True

    userQuestionRel.create(user=current_user.id, question=ID, correctAnswer=answeredCorrectly)

    return render_template('resultat.html', question_text=question.questionText, answerText=answer, answer=answeredCorrectly)


# For hver gang der kommer en 401 error på vores hjemmeside bliver denne funktion kaldt!
# Lige nu forventer vi at alle 401 errors har noget at gøre med at man som bruger ikke er logget ind!
@app.errorhandler(401)
def unauthorized(error):
    return render_template('errors/401.html'), 401


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
