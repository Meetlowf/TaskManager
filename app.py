from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

import decimal
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.secret_key = 'bruh'
db = SQLAlchemy(app)

def convert_sqlobj_json(obj):
    """Convert the result of the SQLAlchemy query to Json"""
    recs = []
    result = [d.__dict__ for d in obj]
    for r in result:
        recs.append(convert_one_sqlobj_json(r))
    return recs

def convert_one_sqlobj_json(r):
    while "_sa_instance_state" in r:
        r.pop("_sa_instance_state")
        for k, v in r.items():

            if isinstance(v, type(datetime.date)):
                """ Date format """
                r[k] = v.isoformat()

            elif isinstance(v, str):
                """ Check for Double quotes, it break the Json format if don't replaced for '\\"' """
                if '"' in v:
                    r[k] = v.replace('"', '\\"')
                elif "\r\n" in v:
                    r[k] = v.replace("\r\n", "<br>")
            elif v == None:
                r[k] = ""
            elif isinstance(v, decimal.Decimal):
                r[k] = str(v)
        return r

# @app.route("<id>")
# def list_all(id):
# tasks = Task.query.filter_by(projectid=id).all()
#     records = convert_sqlobj_json(tasks)
#     return render_template("tasks.html", records=records)

class ProjectForm(FlaskForm):
    content = StringField('New Project:', validators=[DataRequired()])
    date = DateField('Date Due:', validators=[DataRequired()], format='%Y-%m-%d')

class TaskForm(FlaskForm):
    content = StringField('New Task:', validators=[DataRequired()])
    date = DateField('Date Due:', validators=[DataRequired()], format='%Y-%m-%d')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Tasks', backref='owner', lazy='dynamic', cascade="all, delete-orphan")
    date_due = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Project %r>' % self.id

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    date_due = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    form = ProjectForm()
    if request.method =='POST':
        project_name = form.content.data
        date_picked = form.date.data.strftime('%Y-%m-%d')
        new_project = Project(name=project_name, date_due=date_picked)
        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect('/task/' + str(new_project.id))
        except:
            return 'There was a problem'
    else:
        projects = Project.query.order_by(Project.date_due).all()
        return render_template('project.html', projects=projects, form=form)

@app.route('/task/<int:id>', methods=['POST', 'GET'])
def task(id):
    project = Project.query.filter_by(id=id).first()
    form = TaskForm()
    if request.method == 'POST':
        task_content = form.content.data
        date_picked = form.date.data.strftime('%Y-%m-%d')
        new_task = Tasks(content=task_content, project_id=id, date_due=date_picked)
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/task/'+str(id))
        except:
            return 'There was a problem'
    else:
        task_table = Tasks.query.filter_by(project_id=id).all()
        records = convert_sqlobj_json(task_table)
        projects = Project.query.order_by(Project.date_due).all()
        return render_template('task.html', tasks=task_table, project=project, projects=projects, form=form, records=records)

@app.route('/pdelete/<int:id>')
def pdelete(id):
    project_to_delete = Project.query.get_or_404(id)
    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect('/')
    except: 
        return 'There is a problem'

@app.route('/delete/<int:id>/<int:pid>')
def delete(id, pid):
    task_to_delete = Tasks.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/task/'+str(pid))
    except: 
        return 'There is a problem'

@app.route('/update/<int:id>/<int:pid>', methods=['POST'])
def update(id, pid):
    task = Tasks.query.get_or_404(id)
    task.content = request.form['content']
    try:
        db.session.commit()
        return redirect('/task/'+str(pid))
    except:
        return 'There is a problem'

@app.route('/done/<int:id>/<int:pid>')
def done(id, pid):
    task = Tasks.query.get_or_404(id)
    if task.done == 1:
        task.done = 0
        try:
            db.session.commit()
            return redirect('/task/'+str(pid))
        except:
            return 'There is a problem'
    else:
        task.done = 1
        try:
            db.session.commit()
            return redirect('/task/'+str(pid))
        except:
            return 'There is a problem'


if __name__ == "__main__":
    app.run(debug=True)