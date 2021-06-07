from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    content = StringField('New Project:', validators=[DataRequired()])
    date = DateField('Date Due:', validators=[DataRequired()], format='%Y-%m-%d')

class TaskForm(FlaskForm):
    content = StringField('New Task:', validators=[DataRequired()])
    date = DateField('Date Due:', validators=[DataRequired()], format='%Y-%m-%d')
