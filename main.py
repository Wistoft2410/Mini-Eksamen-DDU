from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Man skal have en "secret_key" for at kryptere bruger browser sessionen!
app.secret_key = '387r3q897thghds0-'

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'

bcrypt = Bcrypt(app)


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
            if bcrypt.check_password_hash(user.password, password):
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
    users = User.select()

    for user in users:
        print(user.email)
        print(user.password)

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
            if bcrypt.check_password_hash(user.password, password):
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
            user = User.create(username=name,
                               email=email.lower(),
                               # Hash brugerens adgangskode
                               password=bcrypt.generate_password_hash(password).decode("utf-8"),
                               teacher=(True if checkbox else False))
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
    classes = current_user.classes
    return render_template('test_velkommen.html', classes=classes)


@app.route('/test/<classname>/', methods=('GET', 'POST'))
@login_required
def testen(classname):
    clazz = Class.get(Class.name == classname)

    # Sørg for ikke at finde spørgsmål som eleven allerede har svaret på!
    answered_questions = [data.question for data in userQuestionRel.select().where(userQuestionRel.user == current_user.id)]
    questions = simpleQuestion.select().where((simpleQuestion.clazz == clazz) & (simpleQuestion.id.not_in(answered_questions)))

    if request.method == 'POST':
        question_datas = []

        ids = request.form.getlist('id[]')
        answers = request.form.getlist('answer[]')

        for index, ID in enumerate(ids): 
            question = simpleQuestion.get_or_none(int(ID))

            answeredCorrectly = False

            if question:
                if question.yesOrNo:
                    if question.answer1 == answers[index]:
                        answeredCorrectly = True

                elif question.answer2 == answers[index]:
                    answeredCorrectly = True

            userQuestionRel.create(user=current_user.id, question=ID, correctAnswer=answeredCorrectly)
            question_datas.append({"question": question, "correct": answeredCorrectly, "answer": answers[index]})

        return render_template('resultat.html', questions=question_datas)
    return render_template('test.html', questions=questions, classname=classname)


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

        question_id = simpleQuestion.create(clazz=class_id,
                                            questionText=question,
                                            answer1=answer1,
                                            answer2=answer2,
                                            yesOrNo=yesOrNo)

        flash("Spørgsmål er lavet! ✔")

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
    user_ids = [rel.user.id for rel in userClassRel.select().join(User, on=(User.id == userClassRel.user.id))]
    users_with_no_classes = User.select().where(~(User.teacher) & User.id.not_in(user_ids))

    classes = Class.select()

    return render_template('teacher_student_list.html', users=users_with_no_classes, classes=classes)


@app.route('/delete_user', methods=('POST',))
@login_required
def delete_user():
    user_id = request.form.get('elev_id')
    user = User.get_or_none(User.id == user_id)

    if user:
        user.delete_instance()
        flash("Eleven er blevet slettet!")
    else:
        flash("Der skete en fejl, vi kunne ikke finde den elev")

    return redirect(url_for('elev_uden_klasse_liste'))

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
    app.run(port=int(os.environ.get('PORT', 5000)))
