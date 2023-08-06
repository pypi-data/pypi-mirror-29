# -*- coding: utf-8 -*-
from flask import Flask, render_template, g
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_security.utils import hash_password
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from Mandark.project.config import ProductionConfig
from sqlalchemy.exc import OperationalError
from raven.contrib.flask import Sentry


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app(config_object=ProductionConfig):
    app = Flask(__name__)
    Sentry(app, dsn='https://1fc1a5fea77b4b3c9f4edcf29807e5d4:de25524c893345b1ab6f3fe165131f9e@sentry.io/300199')  # noqa

    CORS(app)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    from Mandark.project import models
    
    userstore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    Security(app, userstore)

    @app.before_request
    def before_request():
        g.user = current_user

    @app.errorhandler(404)
    def not_found_error():
        return render_template('404.html', title='FourOhFour')

    @app.errorhandler(500)
    def internal_error():
        return render_template('500.html', title='A server oops happened')

    try:
        with app.app_context():
            userstore.find_or_create_role(name='admin',
                                          description='Administrator')
            userstore.find_or_create_role(name='user',
                                          description='General User')
            userstore.create_user(email='admin@taiosolve.xyz',
                                  password=hash_password('admin'))
            userstore.create_user(email='user@taiosolve.xyz',
                                  password=hash_password('user'))
            userstore.create_user(email='allan@taiosolve.xyz',
                                  password=hash_password('Allanice-001'))
            userstore.add_role_to_user('admin@taiosolve.xyz', 'admin')
            userstore.add_role_to_user('user@taiosolve.xyz', 'user')
            userstore.add_role_to_user('allan@taiosolve.xyz', 'admin')
            db.session.commit()
            print('IGETHEE')
    except OperationalError:
        if app.debug:
            print(OperationalError)
        else:
            pass
    except Exception as e:
        with app.app_context():
            print(e)
            db.session.rollback()

    from Mandark.project.views import main, admin
    app.register_blueprint(main.main)

    app_admin = Admin(app, 'Administration Section',
                      template_mode='bootstrap3',
                      index_view=admin.MyAdminIndexView())
    app_admin.add_view(admin.UserModelView(models.User, db.session))
    app_admin.add_view(admin.RoleModelView(models.Role, db.session))
    app_admin.add_link(MenuLink(name='Back to Site', url='/'))

    return app
