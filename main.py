from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

app = Flask(__name__)

# Man skal have en "secret_key" for at kryptere bruger browser sessionen!
app.secret_key = '387r3q897thghds0-'

login_manager = LoginManager(app=app)
login_manager.session_protection = 'strong'


from db import User, DB, simpleQuestion, userQuestionRel, userClassRel, Class, IntegrityError


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
                return redirect(url_for('test_velkommen'))
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
            return render_template('teacher_login.html', error_msg="Denne email findes ikke i lærer databasen!")
        else:
            if user.password == password:
                # Det her kører hvis brugeren HAR angivet det rigtige password 
                login_user(user)
                return redirect(url_for('teacher_startside'))
            else:
                # Det her kører hvis brugeren ikke har angivet det rigtige password 
                return render_template('teacher_login.html', error_msg="Denne adgangskode passer ikke!")

    # Det her kører hvis brugeren bare har lavet en "GET" request til denne rute
    return render_template('teacher_login.html')


@app.route('/logud', methods=('GET',))
@login_required
def logout():
    logout_user()
    flash("Vi ses en anden gang!")
    return redirect(url_for('home'))


@app.route('/teacher_startside', methods=('GET',))
@login_required
def teacher_startside():
    return render_template('teacher_startside.html', name=current_user.username)


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
            if user.teacher:
                return redirect(url_for('teacher_startside'))
            else:
                return redirect(url_for('test_velkommen'))
        else:
            return render_template('signup.html', error=True)
    return render_template('signup.html', error=False)


@app.route('/test_velkommen', methods=('GET', 'POST'))
@login_required
def test_velkommen():
    return render_template('test_velkommen.html')


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


@app.route('/opret_flere_questions', methods=('GET', 'POST'))
@login_required
def opret_flere_questions():
    classes = Class.select()

    if request.method == 'POST':
        class_id = request.form.get('klasse_id')
        question = request.form.get('spørgsmål')
        answer1 = request.form.get('svar1')
        answer2 = request.form.get('svar2')
        correct_answer = request.form.get('correctAnswer')

        yesOrNo = True if correct_answer == 'svar1' else False

        question_id = simpleQuestion.create(questionText=question,
                                            answer1=answer1,
                                            answer2=answer2,
                                            correctAnswer=correct_answer,
                                            yesOrNo=yesOrNo)
        flash("Spørgsmål lavet! ✔")

    return render_template('teacher_question_creation.html', classes=classes)


@app.route('/elev_resultat_liste', methods=('GET',))
@login_required
def elev_resultat_liste():
    # Find alle elever der ikke er lærere først
    users = User.select().where(~(User.teacher))

    # Find alle elevers spørgsmåls data
    student_results = [(user.username, retrive_user_test_data(user)) for user in users]

    return render_template('teacher_resultat.html', student_results=student_results)


def retrive_user_test_data(user):
    question_data = userQuestionRel.select().join(User).where(User.id == user).execute()

    retrieved_question_data = [{
            "question": data.question.questionText, 
            "answer1": data.question.answer1, 
            "answer2": data.question.answer2, 
            "correctAnswer": data.question.yesOrNo, 
            "studentsAnswer": data.correctAnswer
        } for data in list(question_data)]

    return retrieved_question_data


@app.route('/elev_uden_klasse_liste', methods=('GET',))
@login_required
def elev_uden_klasse_liste():
    users_with_classes = userClassRel.select(userClassRel.user.id)
    users_with_no_classes = User.select().where(User.id.not_in(users_with_classes) & ~(User.teacher))

    classes = Class.select()

    return render_template('teacher_student_list.html', users=users_with_no_classes, classes=classes)


@app.route('/opret_klasse', methods=('POST',))
@login_required
def opret_klasse():
    class_name = request.form.get('klasse')

    try:
        Class.create(name=class_name)
        flash(f"Klassen {class_name} blev oprettet! 😁")
    except IntegrityError:
        flash("Denne klasse findes allerede, prøv at finde på et nyt navn 😕")

    return redirect(url_for('elev_uden_klasse_liste'))


@app.route('/tildel_klasse', methods=('POST',))
@login_required
def tildel_klasse():
    student_id = request.form.get('elev_id')
    class_id = request.form.get('klasse_id')

    student_name = User.get_by_id(student_id).username
    class_name = Class.get_by_id(class_id).name

    userClassRel.create(user=student_id, clazz=class_id)
    flash(f"Eleven {student_name} er blevet tildelt klassen {class_name} 😁")

    return redirect(url_for('elev_uden_klasse_liste'))

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
