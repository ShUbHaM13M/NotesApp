import os
from itertools import combinations_with_replacement
from os import name

from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, send_file, send_from_directory, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/users'
app.config.from_pyfile('config.py')
app.config['TESTING'] = False
app.config['CSRF_ENABLED'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SeyTonic13'

db = SQLAlchemy(app)

root = os.getcwd()

if not os.path.exists('./Users'):
    os.makedirs('Users')

os.chdir(root)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    path = db.Column(db.String(150))

    def __init__(self, username, password, path, email):
        self.username = username
        self.password = password
        self.path = path
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def splashscreen():
    return render_template('splashscreen.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        if "user" in session:
            os.chdir(get_user_directory())
            file_name = request.form['fileTitle']
            file_content = request.form['fileContent']
            _file_operation(file_name, file_content)
            return redirect(url_for('home'))
    else:
        if "user" in session:
            user = session["user"]
            flash(f'{user}'[0])
            return render_template('index.html')
        return render_template('index.html')


def _file_operation(file_name, file_content):
    file_name = file_name.strip()
    file = open(f"{file_name}", 'w', encoding='utf-8')
    file.write(file_content)
    file.close()


def get_user_directory():
    if "user" in session:
        return session['path']
    else:
        return None


@app.route("/get-file/<name>")
def get_file(name):
    if "user" in session:
        user = session["user"]
    else:
        return redirect(url_for('home'))
    try:
        return send_from_directory(f'./Users/{user}/', filename=name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/delete-file/<name>', methods=["POST", ""])
def delete_file(name):
    os.chdir(session['path'])
    file_name = f"{name.strip()}"
    os.remove(file_name)
    return redirect(url_for('savedNotes'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    os.chdir(root)
    if request.method == "POST":
        user = request.form["un"]
        email = request.form["em"]
        password = request.form["pwd"]
        cpwd = request.form["cpwd"]
        try:
            if password == cpwd:
                os.mkdir(f'./Users/{user}')
                user_path = os.path.abspath(f'./Users/{user}')
                tempUser = User(
                    username=user,
                    password=password,
                    path=user_path,
                    email=email
                )

                db.session.add(tempUser)
                db.session.commit()
                return redirect(url_for('home'))
            else:
                return redirect(url_for('register'))
        except exc.IntegrityError:
            flash('Entered Username is already taken', 'error')
            return redirect(url_for('register'))
        except FileExistsError:
            flash('Entered Username is already taken', 'error')
            return redirect(url_for('register'))

    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form["un"]
        pwd = request.form["pwd"]

        isRegisteredUser = User.query.filter_by(
            username=user, password=pwd).first()
        if isRegisteredUser:
            session['user'] = isRegisteredUser.username
            session['path'] = isRegisteredUser.path
        else:
            flash(u'User not found check username and password again', 'error')
            return redirect(url_for('login'))

        return redirect(url_for('home'))
    else:
        if "user" in session:
            return redirect(url_for('home'))
        return render_template('login.html')


@app.route('/saved-notes', methods=['POST', 'GET'])
def savedNotes():
    if request.method == "POST":
        if "user" in session:
            os.chdir(get_user_directory())
            file_name = request.form['fileTitle']
            file_content = request.form['fileContent']
            _file_operation(file_name, file_content)
            return redirect(url_for('savedNotes'))
    else:
        user = session["user"]
        flash(f'{user}'[0])
        os.chdir(session['path'])
        file_data = [open(f, 'r').read() for f in os.listdir()]
        file_names = [f.rsplit('.')[0] for f in os.listdir()]
        return render_template('saved-notes.html', files=dict(zip(file_names, file_data)))


@app.route('/logout')
def logout():
    if "user" in session:
        session.clear()
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.route('/about')
def about():
    try:
        user = session['user']
        flash(user[0])
    except:
        pass
    return render_template("about.html")


@app.route('/construction')
def construction():
    try:
        user = session['user']
        flash(user[0])
    except:
        pass
    return render_template('under-construction.html')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
