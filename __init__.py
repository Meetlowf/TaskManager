from flask import Flask, session
# from flask_login import LoginManager
from htmlProject import model
from htmlProject import projectFolder
from htmlProject import loginPath

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.secret_key = 'SUPER_SECRET_KEY'
    projectFolder.init_app(app)
    loginPath.init_app(app)
    model.init_app(app)

    return app
