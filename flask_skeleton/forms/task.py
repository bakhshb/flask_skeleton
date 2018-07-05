from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, validators, BooleanField, TextAreaField, SelectField, DateField
from flask_babelex import lazy_gettext
from ..model import User

class TaskForm(FlaskForm):
    name = StringField(lazy_gettext('Name'))
    task_type = SelectField(lazy_gettext('Task Type'), validators=[validators.DataRequired()], coerce=int)
    organization= SelectField(lazy_gettext('Organization'), validators=[validators.DataRequired()], coerce=int )
    place= SelectField(lazy_gettext('Place'), validators=[validators.DataRequired()], coerce=int )
    task_from = DateField(lazy_gettext('Task From'), format='%Y-%m-%d')
    task_to = DateField (lazy_gettext('Task To'), format='%Y-%m-%d')
    result = TextAreaField(lazy_gettext('Result'))


class SearchForm(FlaskForm):
    search = StringField(lazy_gettext('Search'))
    created_from = DateField(lazy_gettext('From'), format='%Y-%m-%d')
    created_to = DateField (lazy_gettext('To'), format='%Y-%m-%d')


class TaskTypeForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[validators.DataRequired()])

class OrganizationForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[validators.DataRequired()])

class PlaceForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[validators.DataRequired()])
