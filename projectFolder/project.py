from flask import  Blueprint, render_template, Flask, url_for, request, redirect, Blueprint, abort, flash
from datetime import datetime
import decimal

from werkzeug.exceptions import UnsupportedMediaType

from htmlProject.model import db
from htmlProject.model.models import Project, Tasks
from htmlProject.forms import ProjectForm, TaskForm, UpdateTaskForm
# from htmlProject.app import convert_sqlobj_json
# from htmlProject.app import convert_one_sqlobj_json

projectRoute = Blueprint("projectRoute", __name__)

@projectRoute.route('/', methods=['POST', 'GET'])
def home():
    form = ProjectForm()
    if request.method =='POST':
        project_name = form.content.data
        date_picked = form.date.data.strftime('%Y-%m-%d')
        new_project = Project(name=project_name, date_due=date_picked)
        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect('/project/' + str(new_project.id))
        except:
            return 'There was a problem'
    else:
        projects = Project.query.order_by(Project.date_due).all()
        return render_template('project.html', projects=projects, form=form)

@projectRoute.route('/<int:id>', methods=['POST', 'GET'])
def task(id):
    project = Project.query.filter_by(id=id).first()
    form = TaskForm()
    form1 = UpdateTaskForm()
    if request.method == 'POST':
        task_content = form.content.data
        date_picked = form.date.data.strftime('%Y-%m-%d')
        new_task = Tasks(content=task_content, project_id=id, date_due=date_picked)
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/project/'+str(id))
        except:
            return 'There was a problem'
    else:
        task_table = Tasks.query.filter_by(project_id=id).all()
        records = convert_sqlobj_json(task_table)
        projects = Project.query.order_by(Project.date_due).all()
        return render_template('task.html', tasks=task_table, project=project, projects=projects, form=form, records=records, form1=form1)

@projectRoute.route('/<int:id>/project_delete')
def pdelete(id):
    project_to_delete = Project.query.get_or_404(id)
    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect('/project/')
    except: 
        return 'There is a problem'

@projectRoute.route('/<int:pid>/task_delete/<int:id>')
def delete(id, pid):
    task_to_delete = Tasks.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/project/'+str(pid))
    except: 
        return 'There is a problem'

@projectRoute.route('/<int:pid>/task_update/<int:id>', methods=['POST'])
def update(id, pid):
    task = Tasks.query.get_or_404(id)
    form = UpdateTaskForm()
    task.content = form.content.data
    task.date_due = form.date.data.strftime('%Y-%m-%d')
    try:
        db.session.commit()
        flash("Success! Task saved.")
        return redirect('/project/'+str(pid))
    except:
        return 'There is a problem'

@projectRoute.route('/<int:pid>/task_done/<int:id>')
def done(id, pid):
    task = Tasks.query.get_or_404(id)
    if task.done == 1:
        task.done = 0
        try:
            db.session.commit()
            return redirect('/project/'+str(pid))
        except:
            return 'There is a problem'
    else:
        task.done = 1
        try:
            db.session.commit()
            return redirect('/project/'+str(pid))
        except:
            return 'There is a problem'

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