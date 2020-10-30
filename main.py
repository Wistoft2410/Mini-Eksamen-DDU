from flask import Flask, render_template

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

@app.route('/test', methods=('GET', 'POST'))
def testen():
    return render_template('test.html')

@app.route('/resultat', methods=('GET', 'POST'))
def resultatet():
    return render_template('resultat.html')

@app.route('/teacher_login', methods=('GET', 'POST'))
def teacher():
    return render_template('teacher_login.html')

if __name__ == '__main__':
    app.run()
