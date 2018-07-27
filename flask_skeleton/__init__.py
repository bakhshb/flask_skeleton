from flask import Flask, request, session, url_for
from flask_babelex import Babel
from flask_admin import Admin, helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect
from flask_assets import Environment
from webassets.loaders import YAMLLoader
from flask_sslify import SSLify
from .util import mail,inject_current_language, inject_all_languages, inject_google_token, \
                         inject_total_notification, inject_tasks, bad_request, page_not_found, page_forbidden, page_server_error
from .model import  db, User, Role, Task, TaskType, Organization, Place, Page, Message
csrf = CSRFProtect()
from .home import home_blueprint
from .page import page_blueprint
from .profile import profile_blueprint
from .user import user_blueprint
from .message import message_blueprint
from .task import task_blueprint
from .admin import AdminIndexCustomView, UserCustomView,\
 RoleCustomView, TaskCustomView, TaskTypeCustomView, OrganizationCustomView,\
 PlaceCustomView, PageCustomView, ReturnToMainView
from .momentjs import momentjs
import os, logging, logging.config, yaml

from .config import app_config

def create_app(ENV_SETTING):
    app = Flask(__name__, instance_relative_config=True)

    #configuration
    app.config.from_object(app_config[ENV_SETTING])

    # Logging configuration
    logging.config.dictConfig(yaml.load(open(app.config['LOGGING_FILEPATH'])))

    # Yaml Loader to load css and js
    assets = Environment(app)
    loader = YAMLLoader(app.config['ASSETS_FILEPATH']).load_bundles()
    load_assets(assets, loader)

    #database init
    db.init_app(app)
    # with app.app_context():
    #     create_user(app,db)
    #flask_admin
    admin = Admin(app, index_view=AdminIndexCustomView(url=None,endpoint=None) , name='Admin Panel', base_template='admin/my_master.html', template_mode='bootstrap3')
    # Mail
    mail.init_app(app)
    # csrf
    csrf.init_app(app)
    #SSL
    sslify = SSLify(app)
    #setting babelex
    babel = Babel(app)
    @babel.localeselector
    def get_locale():
        # if the user has set up the language manually it will be stored in the session,
        # so we use the locale from the user settings
        try:
            language = session['language']
        except KeyError:
            language = None
        if language is not None:
            return language
        return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

    # Inject to JINJA Template
    app.context_processor(inject_current_language)
    app.context_processor(inject_all_languages)
    app.context_processor(inject_google_token)
    app.context_processor(inject_total_notification)
    app.context_processor(inject_tasks)

    # Template Filter
    app.jinja_env.globals['momentjs'] = momentjs

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Integrate Flask Security with Flask Admin
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    # Admin Views
    load_admin_views(admin, db)
    # Blueprint Views
    load_blueprints(app)
    # Register Error Handling
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, page_forbidden)
    app.register_error_handler(500, page_server_error)
    app.logger.info('app started')

    return app

# Blueprint
def load_blueprints (app):
    app.register_blueprint(home_blueprint)
    app.register_blueprint(page_blueprint, url_prefix='/page')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(task_blueprint, url_prefix='/task')
    app.register_blueprint(message_blueprint, url_prefix='/message')

# Admin
def load_admin_views(admin, db):
    admin.add_view(UserCustomView(User, db.session))
    admin.add_view(RoleCustomView(Role, db.session))
    admin.add_view(TaskCustomView(Task, db.session))
    admin.add_view(TaskTypeCustomView(TaskType, db.session))
    admin.add_view(OrganizationCustomView(Organization, db.session))
    admin.add_view(PlaceCustomView(Place, db.session))
    admin.add_view(PageCustomView(Page, db.session))
    admin.add_view(ReturnToMainView(name='Back To Client',url=None,endpoint=None))

# assets
def load_assets(assets, loader):
    assets.register('css_all', loader['bundles-client-css'])
    assets.register('js_all', loader['bundles-client-js'])
    assets.register('admin_css_all', loader['bundles-admin-css'])
    assets.register('admin_js_all', loader['bundles-admin-js'])

# init database tables and create admin user
def create_user(app, db):
    db.create_all()
    if not Role.query.filter(Role.name== app.config['ADMIN_ROLE']).first():
        role = Role(name=app.config['ADMIN_ROLE'])
        db.session.add(role)
        db.session.commit()
    if not User.query.filter(User.email == app.config['ADMIN_EMAIL']).first():
        user = User(firstname=app.config['ADMIN_FIRSTNAME'],lastname=app.config['ADMIN_LASTNAME'],email=app.config['ADMIN_EMAIL'])
        user.hash_password(app.config['ADMIN_PASSWORD'])
        role = Role.query.filter_by(name=app.config['ADMIN_ROLE']).first()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
