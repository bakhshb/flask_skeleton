from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, validators, BooleanField, TextAreaField, SelectField, DateField, SubmitField
from flask_babelex import lazy_gettext

class MessageForm(FlaskForm):
    recipient = SelectField(lazy_gettext('Recipient'), validators=[validators.DataRequired()], coerce=int)
    subject = StringField(lazy_gettext('Subject'))
    message = TextAreaField(lazy_gettext('Message'), validators=[validators.DataRequired(), validators.Length(min=0, max=140)])
    submit = SubmitField(lazy_gettext('Submit'))

class ReplyForm(FlaskForm):
    message = TextAreaField(lazy_gettext('Message'), validators=[validators.DataRequired(), validators.Length(min=0, max=140)])
    submit = SubmitField(lazy_gettext('Submit'))
