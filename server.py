import os
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from models import User, Todo
from settings import app, db



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@app.route('/')
@login_required
def index():
    return render_template('index.html',
                           todos=Todo.query.filter_by(user_id=g.user.id).order_by(Todo.pub_date.desc()).all()
                           )


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            todo = Todo(request.form['title'], request.form['text'])
            todo.user = g.user
            db.session.add(todo)
            db.session.commit()
            flash('Todo item was successfully created')
            return redirect(url_for('index'))
    return render_template('new.html')


@app.route('/todos/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def show_or_update(todo_id):
    todo_item = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template('view.html', todo=todo_item)
    if todo_item.user.id == g.user.id:
        todo_item.title = request.form['title']
        todo_item.text = request.form['text']
        todo_item.done = ('done.%d' % todo_id) in request.form
        db.session.commit()
        return redirect(url_for('index'))
    flash('You are not authorized to edit this todo item', 'error')
    return redirect(url_for('show_or_update', todo_id=todo_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember=remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
