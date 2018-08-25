from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, validators, BooleanField, TextAreaField, SelectField, DateField
from flask_babelex import lazy_gettext

class EditProfileForm(FlaskForm):
    firstname = StringField(lazy_gettext('First Name'), [validators.Length(min=4, max=25)])
    lastname = StringField(lazy_gettext('Last Name'), [validators.Length(min=4, max=25)])
    email = StringField(lazy_gettext('Email Address'), [validators.Email()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('Email is already in use.'))
