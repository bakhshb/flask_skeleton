from flask import url_for, render_template ,redirect, request, abort, current_app
from flask_admin import AdminIndexView, BaseView, expose
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from wtforms import  SelectField


class RequiredBooleanField(SelectField):
    # wtforms/flask-admin has a flaw related
    # to boolean fields with required=True in the model
    # Ultimatelly false values wouldn't pass validation of the form
    # thus the workaround
    def __init__(self, *args, **kwargs):
        choices = [
            (True, "True"),
            (False, "False"),
        ]

        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"

        super(RequiredBooleanField, self).__init__(*args, **kwargs)


# Create customized model view class
class ModelViewCustom(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('Admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminIndexCustomView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        elif current_user.has_role('Admin'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class ReturnToMainView(BaseView):

    @expose('/')
    def index(self):
        return redirect(url_for('home_blueprint.index'))

class UserCustomView(ModelViewCustom):
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    column_exclude_list = ['password', ]
    column_searchable_list = ['firstname', 'email']
    form_excluded_columns = ['password','created_at', 'updated_at', 'last_login_at','current_login_at','last_login_ip', \
                            'current_login_ip', 'login_count','confirmed_at','tasks','versions', 'messages_sent', 'messages_received']
    form_overrides = {
        "active": RequiredBooleanField,
    }


class RoleCustomView(ModelViewCustom):
    can_create = True
    can_edit = True
    can_delete = False
    column_searchable_list = ['name',]



class TaskCustomView(ModelViewCustom):
    can_create = True
    can_edit = True
    can_delete = False
    can_export = True
    column_searchable_list = ['created_at', 'start_date', 'end_date',]
    form_excluded_columns = ['created_at', 'updated_at',]
    form_widget_args = {
        'result': {
            'class': 'textarea'
        }
    }
class TaskTypeCustomView(ModelViewCustom):
    can_create = True
    can_edit = True
    can_delete = False
    column_searchable_list = ['name',]
    form_excluded_columns = ['created_at', 'updated_at',]

class OrganizationCustomView(ModelViewCustom):
    can_create = True
    can_edit = True
    can_delete = False
    column_searchable_list = ['name',]
    form_excluded_columns = ['created_at', 'updated_at',]

class PlaceCustomView(ModelViewCustom):
    can_create = True
    can_edit = True
    can_delete = False
    column_searchable_list = ['name',]
    form_excluded_columns = ['created_at', 'updated_at',]

class PageCustomView(ModelViewCustom):
    column_searchable_list = ['url','title','created_at',]
    form_excluded_columns = ['created_at', 'updated_at',]
    form_overrides = {
        "publish": RequiredBooleanField,
    }
    form_widget_args = {
        'content': {
            'class': 'textarea'
        }
    }
