from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from flask_security import login_required, roles_required
from datetime import date, datetime
from .forms import TaskForm, SearchForm, TaskTypeForm, OrganizationForm, PlaceForm
from ..model import db, User, Task, TaskType, Organization, Place


task_blueprint = Blueprint('task_blueprint', __name__)

#
def populate_form_choices(task_form):
    """
    Pulls choices from the database to populate our select fields.
    """
    tasks_type = TaskType.query.all()
    organizations = Organization.query.all()
    places = Place.query.all()
    task_type_names = []
    for task_type in tasks_type:
        task_type_names.append(task_type.name)
    #choices need to come in the form of a list comprised of enumerated lists
    #example [('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    task_type_choices = list(enumerate((task_type_names),1))
    organization_names = []
    for organization in organizations:
        organization_names.append(organization.name)
    organization_choices = list(enumerate((organization_names),1))
    place_names = []
    for place in places:
        place_names.append(place.name)
    place_choices = list(enumerate((place_names),1))
    #now that we've built our choices, we need to set them.
    task_form.task_type.choices = task_type_choices
    task_form.organization.choices = organization_choices
    task_form.place.choices = place_choices


@task_blueprint.route('/', methods=['GET'])
def get_task ():
    form = SearchForm(request.form)
    tasks = Task.query.all()
    return render_template('task/index.html', tasks=tasks, search_form=form)


@task_blueprint.route('/add', methods=['GET', 'POST'])
def add_task ():
    form = TaskForm(request.form)
    task_type_form = TaskTypeForm(request.form)
    organization_form = OrganizationForm(request.form)
    place_form = PlaceForm(request.form)
    populate_form_choices(form)
    if form.validate_on_submit():
        user_id = current_user.id
        task_type = form.task_type.data
        organization = form.organization.data
        place = form.place.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        results= form.results.data
        task = Task(user_id =user_id, task_type_id=task_type, organization_id=organization, place_id=place, start_date=start_date, end_date=end_date, results=results)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('task_blueprint.get_task'))
    return render_template('task/add.html', task_form=form, task_type_form = task_type_form,\
                                                        organization_form = organization_form,\
                                                        place_form = place_form)


# Add New Task Type
@task_blueprint.route('/tasktype', methods=['POST'])
def add_task_type():
    form = TaskTypeForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        task_type = TaskType(name = name)
        db.session.add(task_type)
        db.session.commit()
        return redirect(url_for('task_blueprint.add_task'))
    return redirect(url_for('task_blueprint.add_task'))
# Add New organization
@task_blueprint.route('/organization', methods=['POST'])
def add_organization():
    form = OrganizationForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        organization = Organization(name = name)
        db.session.add(organization)
        db.session.commit()
        return redirect(url_for('task_blueprint.add_task'))
    return redirect(url_for('task_blueprint.add_task'))
# Add New Place
@task_blueprint.route('/place', methods=['POST'])
def add_place():
    form = PlaceForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        place = Place(name = name)
        db.session.add(place)
        db.session.commit()
        return redirect(url_for('task_blueprint.add_task'))
    return redirect(url_for('task_blueprint.add_task'))


# Search
@task_blueprint.route('/search', methods=['POST'])
def search_task ():
    # Variables
    form = SearchForm(request.form)
    tasks = Task.query.all()
    if form.validate_on_submit():
        tasks = Task.query.join(User).join(TaskType).join(Organization).join(Place).filter((User.firstname == form.search.data) |\
                (User.lastname == form.search.data)|(TaskType.name == form.search.data)| (Organization.name == form.search.data) | (Place.name == form.search.data) |\
                (Task.created_at.between( form.start_date.data, form.end_date.data))).all()
        return render_template('task/index.html', tasks=tasks, search_form=form)
    return render_template('task/index.html', tasks=tasks, search_form=form)
