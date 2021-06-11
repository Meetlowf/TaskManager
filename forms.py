from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class ProjectForm(FlaskForm):
    content = StringField('New Project:', validators=[DataRequired()])
    date = DateField('Date Due:', validators=[DataRequired()], format='%Y-%m-%d')

class TaskForm(FlaskForm):
    content = StringField('New Task:', validators=[DataRequired()])
    date = DateField('Date Due:', validators=[DataRequired()], format='%Y-%m-%d')

class UpdateTaskForm(FlaskForm):
    content = StringField('Update Task:', validators=[DataRequired()])
    date = DateField('Date Due:', validators=[DataRequired()], format='%Y-%m-%d')

# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(),Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')