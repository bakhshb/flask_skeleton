from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, validators, BooleanField, TextAreaField, SelectField, DateField, ValidationError
from flask_babelex import lazy_gettext
from ..model import User


class RegistrationForm(FlaskForm):
    firstname = StringField(lazy_gettext('First Name'), [validators.Length(min=4, max=25)])
    lastname = StringField(lazy_gettext('Last Name'), [validators.Length(min=4, max=25)])
    email = StringField(lazy_gettext('Email Address'), [validators.Email()])
    password = PasswordField(lazy_gettext('Password'), [
        validators.DataRequired(),
        validators.Length(min=3, max=8),
        validators.EqualTo('confirm_password', message=lazy_gettext('Passwords must match'))
    ])
    confirm_password = PasswordField(lazy_gettext('Confirm Password'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('Email is already in use.'))
