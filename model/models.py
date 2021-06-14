from . import db
from datetime import datetime
# from flask_login import UserMixin

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Tasks', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    date_due = db.Column(db.String(200), nullable=False)
    session_email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Project %r>' % self.id

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    date_due = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))