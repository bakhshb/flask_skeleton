from flask import redirect, url_for, render_template, flash, session, request, current_app
from functools import wraps
from flask_login import current_user
from flask_mail import Mail, Message as MSG
from threading import Thread
from flask_babelex import _
from oauth2client.service_account import ServiceAccountCredentials
from .model import Message, Task
from datetime import datetime
# Check if user already logged in
def already_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            flash(u'You are already logged in!','danger')
            return redirect(url_for('routes.index'))
        else:
            return f(*args, **kwargs)
    return wrap

# Email
mail = Mail()
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def email (subject, body, sender, recipients):
    msg = MSG(subject = subject,  sender=sender, recipients=[recipients])
    msg.html= body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
    current_app.logger.info('Email Sent')

# Google Token
# The scope for the OAuth2 request.
SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
# Defines a method to get an access token from the ServiceAccount object.
def get_access_token():
  return ServiceAccountCredentials.from_json_keyfile_name(\
            current_app.config['GOOGLE_KEY_FILEPATH'], SCOPE\
  ).get_access_token().access_token

def inject_google_token():
    return dict(ACCESS_TOKEN_FROM_SERVICE_ACCOUNT = get_access_token())

# Inject Languags into html jinja
def inject_current_language():
    return dict(CURRENT_LANGUAGE=session.get('language',request.accept_languages.best_match(current_app.config['LANGUAGES'].keys())))

def inject_all_languages():
    return dict(AVAILABLE_LANGUAGES= current_app.config['LANGUAGES'].keys())
# inject Notifications Number
def inject_total_notification():
    if current_user.is_authenticated:
        msgs= current_user.messages_received.order_by(Message.timestamp.desc()).all()
    else:
        msgs = None

    return dict(Message = msgs)

# inject tasks
def inject_tasks():
    return dict(Tasks = Task.query.limit(5))


#Error errorhandler
def bad_request(e):
    return render_template('/400.html'), 400

def page_not_found(e):
    return render_template('/404.html'), 404

def page_forbidden(e):
    return render_template('/403.html'), 403

def page_server_error(e):
    return render_template('/500.html'), 500
