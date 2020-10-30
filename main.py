from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=('GET',))
def home():
    return render_template('hovedmenu.html')


@app.route('/layout', methods=('GET',))
def layout():
    return render_template('layout.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('login.html')

@app.route('/startside', methods=('GET', 'POST'))
def start():
    return render_template('startside.html')

@app.route('/test', methods=('GET', 'POST'))
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run()
