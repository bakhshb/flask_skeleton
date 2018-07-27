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
        task_from = form.task_from.data
        task_to = form.task_to.data
        result = form.result.data
        task = Task(user_id =user_id, task_type_id=task_type, organization_id=organization, place_id=place, task_from=task_from, task_to=task_to, result=result)
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

# Check Search Fileds
def check_fields (created_from, created_to):
    if created_from:
        created_from = datetime.strptime(request.args.get('created_from'),'%Y-%m-%d')
        if created_to:
            created_to = datetime.strptime(request.args.get('created_to'),'%Y-%m-%d')
            return created_from, created_to
        else:
            created_to = datetime(created_from.year, created_from.month +1, created_from.day+5)
            return created_from, created_to

    elif created_to:
        created_to = datetime.strptime(request.args.get('created_to'),'%Y-%m-%d')
        created_from = datetime(created_to.year, created_to.month -1, created_to.day)
        return created_from, created_to
    else:
        today = datetime.today()
        created_from = datetime(today.year, today.month, 1)
        created_to = datetime(today.year, today.month +1, 1)
        return created_from, created_to

# Search
@task_blueprint.route('/search', methods=['GET'])
def search_task ():
    # Variables
    form = SearchForm(request.form)
    search = request.args.get('search')
    created_from = request.args.get('created_from')
    created_to = request.args.get('created_to')
    # Check if fields are empty
    if search == '' and  created_from == '' and  created_to == '':
        tasks = Task.query.all()
        return render_template('task/index.html', tasks=tasks, search_form=form)
    created_from, created_to = check_fields (created_from, created_to)
    # Task Search
    tasks = Task.query.join(User).join(TaskType).join(Organization).join(Place).filter((User.firstname == search) |\
            (User.lastname == search)|(TaskType.name == search)| (Organization.name == search) | (Place.name == search) |\
            (Task.created_at.between( created_from, created_to))).all()
    return render_template('task/index.html', tasks=tasks, search_form=form)
