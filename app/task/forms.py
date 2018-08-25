from flask import flash
from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, validators, BooleanField, TextAreaField, SelectField, DateField, ValidationError
from flask_babelex import lazy_gettext
from ..model import User

class TaskForm(FlaskForm):
    name = StringField(lazy_gettext('Name'))
    task_type = SelectField(lazy_gettext('Task Type'), validators=[validators.DataRequired()], coerce=int)
    organization= SelectField(lazy_gettext('Organization'), validators=[validators.DataRequired()], coerce=int )
    place= SelectField(lazy_gettext('Place'), validators=[validators.DataRequired()], coerce=int )
    start_date = DateField(lazy_gettext('Start Date'), format='%Y-%m-%d', validators=[validators.DataRequired()])
    end_date = DateField (lazy_gettext('End Date'), format='%Y-%m-%d', validators=[validators.DataRequired()])
    results = TextAreaField(lazy_gettext('Results'))

    def validate_end_date (self, field):
        if self.start_date.data > field.data:
            raise ValidationError (lazy_gettext('End date should be greater than Start date'))


class SearchForm(FlaskForm):
    search = StringField(lazy_gettext('Search'))
    start_date = DateField(lazy_gettext('From'), format='%Y-%m-%d',validators=[validators.Optional()])
    end_date = DateField (lazy_gettext('To'), format='%Y-%m-%d',validators=[validators.Optional()])

    def validate_start_date(self,field):
        if self.start_date.data is not None and self.end_date.data is None:
            flash(lazy_gettext('End date value not valid'), 'danger')

    def validate_end_date (self, field):
        if self.end_date.data is not None:
            if self.start_date.data > self.end_date.data:
                print('End date should be greater than Start date')
                raise ValidationError (lazy_gettext('End date should be greater than Start date'))



class TaskTypeForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[validators.DataRequired()])

class OrganizationForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[validators.DataRequired()])

class PlaceForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[validators.DataRequired()])
