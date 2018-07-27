from flask import Blueprint, render_template, session, redirect, \
                url_for, send_from_directory, request, abort, current_app
import os
from flask_login import login_required
from .page import view_flatpage
from ..model import db, Page

home_blueprint = Blueprint('home_blueprint', __name__)

# send favicon
@home_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(home_blueprint.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@home_blueprint.route('/')
@login_required
def index():
    index = Page.query.filter_by(url='home').first()
    if index:
        return view_flatpage(index.url)
    return render_template('index.html')

#Change language
@home_blueprint.route('/<string:language>')
def set_language(language=None):
    previous_url = request.referrer or url_for('home_blueprint.index')
    if not language in current_app.config['LANGUAGES'].keys():
        session['language']='en'
        abort(404)
    session['language'] = language
    return redirect(previous_url)
