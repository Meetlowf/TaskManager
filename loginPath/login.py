from flask import  Blueprint, render_template, request, redirect, flash, Flask, url_for, Response, session
from datetime import datetime
# from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import decimal

from htmlProject.model import db
from htmlProject.model.models import Project, Tasks, User
from htmlProject.forms import ProjectForm, TaskForm, UpdateTaskForm #, LoginForm

loginRoute = Blueprint("loginRoute", __name__)

# session['user']

@loginRoute.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user or not (password == user.password):
            flash('Incorrect email or password')
            return redirect('/login/')
        else:
            session['user'] = email
            return redirect('/project')
    return render_template('login.html')

@loginRoute.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        print("test")
        if user: #email already in use
            flash('Email address already exists')
            print("test1")
            return redirect('/login/signup')
        new_user = User(email=email, name=name, password=password)
        try:
            print("test2")
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login/')
        except:
            return 'There was a problem'
    return render_template('signup.html')

@loginRoute.route('/logout')
def logout():
    session['user'] = ""
    return redirect('/login')