from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, validators, BooleanField, TextAreaField, SelectField, DateField
from flask_babelex import lazy_gettext


class RegistrationForm(FlaskForm):
    firstname = StringField(lazy_gettext('First Name'), [validators.Length(min=4, max=25)])
    lastname = StringField(lazy_gettext('Last Name'), [validators.Length(min=4, max=25)])
    email = StringField(lazy_gettext('Email Address'), [validators.Email()])
    password = PasswordField(lazy_gettext('New Password'), [
        validators.DataRequired(),
        validators.Length(min=3, max=16),
        validators.EqualTo('confirm', message=lazy_gettext('Passwords must match'))
    ])
    confirm = PasswordField(lazy_gettext('Repeat Password'))
