#!/usr/bin/env python3

import argparse
import glob
import hashlib
import os
import re

import dotenv
import loguru

from flask import Flask, request, send_file, render_template, redirect, session

from plugins.database import Database
from routes.class_route import ClassHandler
from auth.auth import authenticate


logger = loguru.logger
dotenv.load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))


available_tests = set()


def passencrypt(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        bytes(password, 'utf-8'),
        bytes(os.getenv('SALT'), 'utf-8'),
        200000
    )


def create_classes_db():
    with Database() as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS classes
            (class varchar(30) not null, name varchar(30), primary key (class))"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS assignments
            (assignment varchar(30) not null,
            name varchar(30),
            class varchar(30) not null,
            foreign key (class) references classes(class),
            primary key (assignment, class))"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS attempts
            (attempt INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment varchar(30) not null,
            user varchar(60) not null, data text,
            score integer default 0,
            maxscore integer not null,
            foreign key (assignment) references assignments(assignment),
            foreign key (user) references users(username)
            )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS registry
            ( user varchar(30) not null,
            class varchar(30) not null,
            primary key (user, class),
            foreign key (user) references users(user),
            foreign key (class) references classes(class))
            """
        )


def create_assignment(class_name, assignment_id, name=""):
    with Database() as db:
        try:
            db.execute(
                """insert into classes (class) values (?)""", [class_name])
        except:
            logger.info("{} already in db", class_name)
        try:
            db.execute("""insert into assignments (class, assignment, name) values (?, ?, ?)""",
                       [class_name, assignment_id, name])
        except:
            logger.info("{} {} already in db", class_name, assignment_id)


def parse_tests(tests):
    for path in tests:
        if os.path.isfile(os.path.join(path, 'prompt.md')):
            class_name, assignment_name = path.split('/')[1:]
            create_assignment(class_name, assignment_name)
            available_tests.add('/'.join(path.split('/')[1:]))


@app.route('/dashboard')
@authenticate
def dashboard():
    data = {"user": session.get("user", None)}
    return render_template('dashboard.html', data=data)


@app.route('/signout')
def signout():
    try:
        session.pop('user', None)
    except Exception as e:  # calling /logout with no session
        logger.error(e)
    return redirect('/')


@app.route('/static/<path:path>')
def get_static_resource(path):
    return send_file(os.path.join(app.root_path, 'static', path))


@app.route('/')
def index():
    data = {"user": session.get("user")}
    return render_template('index.html', data=data)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        with Database() as db:
            email_re = re.compile(
                r'([A-Za-z]{2,3}[0-9]{2,5}|[A-Za-z]{2,}|([A-Za-z]+\.){1,2}[A-Za-z]+)@drexel\.edu')
            pass_re = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}')

            form = request.form.to_dict()
            logger.info(form)
            email = form['email'].strip()
            res = db.get_user(email)

        if res is not None:
            return render_template('register.html', data={}, message="User with that email already exists")
        password = form["password"].strip()
        name = form["name"].strip()
        if any([not pass_re.match(password), not email_re.match(email), len(name) == 0]):
            message = ""
            if not email_re.match(email):
                message = "Email is not an @drexel.edu email"
            elif not pass_re.match(password):
                message = "Password is not secure enough"
            elif len(name) == 0:
                message = "Name was not supplied"
            return render_template('register.html', data={}, message=message)

        password = passencrypt(password)

        # create user and set session id
        with Database() as db:
            db.create_user(str(email), str(password.hex()), str(name))
        session['user'] = {"name": name, "email": email}

        return redirect('/dashboard')
    return render_template('register.html', data={}), 200


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        form = request.form.to_dict()
        username = form.get("username")
        password = form.get("password")
        user_data = None
        with Database() as db:
            user_data = db.get_user(username)

        # failed to sign in
        if user_data is None or user_data.get('password') != passencrypt(password).hex():
            return render_template('signin.html', data={}, message='Failed to sign in')

        # do user auth and set creds
        session['user'] = {"name": user_data.get('name'), "email": username}
        return redirect('/dashboard')
    return render_template('signin.html', data={}), 200


@app.errorhandler(404)
def page_not_found(e):
    data = {"user": session.get("user", None)}
    return render_template('404.html', data=data), 404


@app.errorhandler(401)
def not_signed_in(e):
    data = {"user": session.get("user", None)}
    return render_template('signin.html', data=data), 401


def init_assignments():
    logger.info("Loading available assignments")
    parse_tests(glob.glob(f'{os.getenv("TEST_DIR")}/**/*'))
    logger.info("Assignments loaded: {}", len(available_tests))
    create_classes_db()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="port", default=8163, type=int)
    parser.add_argument("--prod", dest="debug",
                        default=True, action="store_false")
    args = parser.parse_args()

    init_assignments()

    routes = [
        ClassHandler(available_tests)
    ]

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, not_signed_in)
    for route in routes:
        app.register_blueprint(route.route(), template_folder='templates')

    app.run(host="0.0.0.0", port=args.port, debug=args.debug)
