from itertools import combinations_with_replacement
import os
from os import name
import re

from flask import (Flask, flash, redirect,  render_template,
                   request, session, url_for, jsonify,
                   send_from_directory,
                   send_file,
                   abort)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SeyTonic13'

db = SQLAlchemy(app)

root = os.getcwd()

if not os.path.exists('./Users'):
    os.makedirs('Users')

if not os.path.exists('./Users/Guest'):
    os.chdir('./Users')
    os.mkdir('Guest')
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
            os.chdir(session['path'])
            file_name = request.form['fileTitle']
            file_content = request.form['fileContent']
            file = open(f"{file_name}.txt", 'w', encoding='utf-8')
            file.write(file_content)
            file.close()
            return redirect(url_for('home'))

        else:
            os.chdir(f'{root}/Users/Guest')
            file_name = request.form['fileTitle']
            file_content = request.form['fileContent']
            file = open(f'{file_name}.txt', 'w', encoding='utf-8')
            file.write(file_content)
            file.close()
            return redirect(url_for(f"get_file", name=file_name))

    else:
        if "user" in session:
            user = session["user"]
            flash(f'{user}')
            return render_template('index.html')
        return render_template('index.html')


@app.route("/get-file/<name>")
def get_file(name):
    file_name = f"{name}.txt"
    if "user" in session:
        user = session["user"]
    else:
        user = "Guest"
    try:
        return send_from_directory(f'./Users/{user}/', filename=file_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/delete-file/<name>', methods=["POST", ""])
def delete_file(name):
    os.chdir(session['path'])
    file_name = f"{name.strip()}.txt"
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
            return f'{user} already taken'
        except FileExistsError:
            return f'{user} already taken'

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
            return "already logged in"
        return render_template('login.html')


@app.route('/saved-notes')
def savedNotes():
    user = session["user"]
    flash(f'{user}')
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
        flash(user)
    except:
        pass
    return render_template("about.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
