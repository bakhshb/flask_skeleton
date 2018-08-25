from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from flask_babelex import _
from .forms import RegistrationForm
from ..model import db, User
from ..util import already_logged_in


user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/register', methods=['GET', 'POST'])
@already_logged_in
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        try:
            user = User(firstname= firstname, lastname= lastname, email=email)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            flash(_(u'Thanks for registering'),'success')
        except:
            flash(_(u'The email is already exist in our system'),'danger')
            return redirect(url_for('user_blueprint.register'))
        return redirect(url_for('security.login'))

    return render_template('security/register_user.html', register_user_form=form)
