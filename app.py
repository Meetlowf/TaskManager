from flask import Flask, render_template, url_for, request, redirect, Blueprint, abort
from datetime import datetime
from htmlProject import model
from htmlProject import projectFolder

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.secret_key = 'SUPER_SECRET_KEY'
    projectFolder.init_app(app)
    model.init_app(app)
    return app
