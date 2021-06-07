from .project import projectRoute

def init_app(app):    
    app.register_blueprint(projectRoute, url_prefix="/project") 