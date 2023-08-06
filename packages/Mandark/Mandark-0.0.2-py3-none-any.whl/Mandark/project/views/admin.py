from flask_admin import AdminIndexView, BaseView
from flask_security import current_user, utils
from flask_admin.contrib.sqla.view import ModelView
from flask import redirect, url_for, flash
from wtforms import PasswordField, validators, StringField


class AdminBaseView(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            flash("You don't have permissions to go there", category="warning")
            return redirect(url_for('main.index'))


class MyAdminIndexView(AdminIndexView, AdminBaseView):
    pass


class AdminModelView(ModelView, AdminBaseView):
    pass


class UserModelView(AdminModelView):
    column_exclude_list = ['password']
    form_excluded_columns = ['last_login_at', 'current_login_at',
                             'last_login_ip', 'current_login_ip',
                             'login_count']
    form_overrides = dict(password=PasswordField)
    form_extra_fields = {'password2': PasswordField('Confirm Password',
                                                    [validators.EqualTo(
                                                        'password',
                                                        message='Passwords must match')]),  # noqa
                         'first_name': StringField('First Name', [validators.DataRequired()]),  # noqa
                         'last_name': StringField('Last Name', [validators.DataRequired()]),  # noqa
                         }
    form_columns = ('first_name', 'last_name', 'roles', 'email', 'password',
                    'password2', 'active')

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = utils.hash_password(model.password)


class RoleModelView(AdminModelView):
    pass
