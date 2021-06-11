from .login import loginRoute

def init_app(app):
    app.register_blueprint(loginRoute, url_prefix="/login")