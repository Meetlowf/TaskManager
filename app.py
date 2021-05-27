from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.secret_key = 'bruh'
db = SQLAlchemy(app)

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
        projects = Project.query.order_by(Project.date_due).all()
        return render_template('task.html', tasks=task_table, project=project, projects=projects, form=form)

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

@app.route('/update/<int:id>/<int:pid>', methods=['GET', 'POST'])
def update(id, pid):
    task = Tasks.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/task/'+str(pid))
        except:
            return 'problem'
    else:
        return render_template('update.html', task=task, pid=pid)

if __name__ == "__main__":
    app.run(debug=True)