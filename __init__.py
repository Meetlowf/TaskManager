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

    # login_manager = LoginManager()
    # login_manager.login_view = 'loginRoute.login'
    # login_manager.init_app(app)

    # from htmlProject.model.models import User

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    return app
