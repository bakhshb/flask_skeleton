from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from flask_security import login_required
from flask_babelex import _
from .forms import EditProfileForm
from ..model import db

profile_blueprint = Blueprint('profile_blueprint', __name__)


@profile_blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile ():
    #fill the form
    user = current_user.query.first_or_404()
    form = EditProfileForm(request.form)
    form.firstname.data = user.firstname
    form.lastname.data = user.lastname
    form.email.data = user.email
    #update
    if form.validate_on_submit():
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        try:
            user.firstname = firstname
            user.lastname= lastname
            user.email=email
            db.session.commit()

            flash(_(u'Your details has been updated'),'success')
        except:
            flash(_(u'The email is already exist in our system'),'danger')
            return redirect(url_for('profile_blueprint.edit_profile'))
        return redirect(url_for('profile_blueprint.view_profile'))
    return render_template('/profile/edit.html', edit_profile_form=form)

@profile_blueprint.route('/view', methods=['GET'])
@login_required
def view_profile ():
    #fill the form
    user = current_user.query.first_or_404()
    form = EditProfileForm(request.form)
    form.firstname.data = user.firstname
    form.lastname.data = user.lastname
    form.email.data = user.email
    return render_template('/profile/view.html', edit_profile_form=form)
