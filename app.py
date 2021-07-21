#!python
# -*- coding: utf-8 -*-

#----------------------------------------

from flask import Flask, jsonify, request
from flask import abort
from flask import make_response
from flask import url_for
from flask_httpauth import HTTPBasicAuth
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp
import logging

# -----------------------------------------------------------------------------

# auxiliary functions

# connects app to config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    return app

# Makes uri in response

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

# -----------------------------------------------------------------------------

# creation block
 
auth = HTTPBasicAuth()
app = create_app()


f_handler = logging.FileHandler('file.log')
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s\
    %(name)s %(threadName)s : %(message)s'))
app.logger.addHandler(f_handler)

# -----------------------------------------------------------------------------

# Error handlers

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def method_not_allowed():
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


@app.errorhandler(405)
def method_not_allowed():
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

# -----------------------------------------------------------------------------

# database block 

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=False)  
    done = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<User %s>' % self.title
 
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %s>' % self.name
 
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password
        }

# -----------------------------------------------------------------------------

# Verification user and password

@auth.verify_password
def verify_password(username, password):
    match = User.query.filter(User.name==username)
    if match and username != '' and password != '':
        try:
            check_password_hash(match[0].password, password)
            app.logger.info('successfully logged in as : ' + match[0].name)
        except:
            app.logger.exception('wrong name or password')
            abort(400)
    else:
        app.logger.warning('Operation failed, prob reason - no user, or empty password')
        abort(400)
    return username

# -----------------------------------------------------------------------------

# routes block

# Get one task

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = Task.query.get(task_id)
    app.logger.info('request on tasks')
    if task == 0:
        app.logger.warning('Operation failed')
        abort(404)
    app.logger.info('Task with id: ' + str(task.id) + ' and title ' + task.title + ' shown')
    return jsonify({'task': make_public_task(task.to_json())})

# GET for all tasks

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    tasks = Task.query.order_by(Task.id.desc()).all()
    app.logger.info('request on tasks')
    return jsonify({'tasks': list(map(make_public_task,map(Task.to_json, tasks)))})

# chek on work main page

# @app.route('/')
# def index():
#     return "Hello, World!"

# POST for tasks

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    app.logger.info('Task creation...')
    if not request.json or not 'title' in request.json:
        app.logger.warning(' Empty or empty title ')
        abort(400)

    title = request.json['title']
    description = request.json['description']
    task = Task(title = title, description = description, done = False)

    try:
        db.session.add(task)
        db.session.commit()
        task = task.to_json()

        task['done'] = True
        app.logger.info('New task ' + task['title']+ ' created')       
    except:
        app.logger.exception('Operation failed')
        return method_not_allowed()
    return jsonify({'task': task})

# PUT for tasks

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    app.logger.info('Task update...')
    task = Task.query.get(task_id)
    if task == 0:
        app.logger.warning('Task is empty')
        abort(404)
    if not request.json:
        app.logger.warning('No request.json')
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        app.logger.warning('Title in request.json id not json and not str')
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        app.logger.warning('Description in request.json id not json and not str')
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        app.logger.warning('Done in request.json id not json and not bool')
        abort(400)

    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    try:
        db.session.commit()
        app.logger.info('Task with id: ' + str(task.id) + ' and title '\
            + task.title + ' is up to date')       
    except :
        app.logger.exception('Operation failed')
        return method_not_allowed()
    return jsonify({'task': task.to_json()})

# Task delete

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    app.logger.info('Task delete...')
    task = Task.query.get_or_404(task_id)
    try:
        db.session.delete(task)
        db.session.commit()
        app.logger.info('Task with id: ' + str(task.id) + ' and title '\
            + task.title + ' successfully deleted')
    except:
        app.logger.exception('Operation failed')
        abort(404)
    
    return jsonify({'result': True})

# -----------------------------------------------------------------------------

# routes for users

# Add a user

@app.route('/todo/api/v1.0/users', methods=['POST'])
@auth.login_required
def create_user():
    app.logger.info('User creating...')
    if not request.json or not 'name' in request.json \
             or request.json['secret_key'] != app.config['SECRET_KEY_FOR_USER_CREATING']:
        app.logger.warning('Not json, or not name in json...')
        abort(400)

    name = request.json['name']
    password = generate_password_hash(request.json['password'])
    user = User(name = name, password = password)
    try:
        db.session.add(user)
        db.session.commit()
        app.logger.info('New user with name ' + user.name + ' successfully created')
        return jsonify({'user': user.to_json()})
    except:
        app.logger.exception('Operation failed')
        return method_not_allowed()

# Delete user

@app.route('/todo/api/v1.0/users/<int:users_id>', methods=['DELETE'])
@auth.login_required
def delete_user(users_id):
    app.logger.info('User delete...')
    user = User.query.get_or_404(users_id)
    if not request.json:
        app.logger.warning('No request.json')
        abort(400)
    if request.json['secret_key'] != app.config['SECRET_KEY_FOR_USERS_DELETE'] :
        app.logger.error('wrong data')   
    try:
        db.session.delete(user)
        db.session.commit()
        app.logger.info('User with id: ' + str(user.id) + ' and name ' + user.name + \
            ' successfully deleted')
    except:
        app.logger.exception('Operation failed')
        abort(404)
    return jsonify({'result': True})

# Get all users

@app.route('/todo/api/v1.0/users', methods=['GET'])
@auth.login_required
def get_users():
    app.logger.info('Get all users...')
    if not request.json:
        app.logger.warning('No request.json')
        abort(400)
    if request.json['secret_key'] == None or \
            request.json['secret_key'] != app.config['SECRET_KEY_FOR_USERS_EXTRACTING'] :
        app.logger.warning('Wrong data')
        abort(400)
    users = User.query.order_by(User.id.desc()).all()
    app.logger.info('Operation get_users success')
    return jsonify({'users': list(map(User.to_json, users))})

# -----------------------------------------------------------------------------

# run

if __name__ == '__main__':
    app.run(host = '127.0.0.1', debug=True, port = 1111)