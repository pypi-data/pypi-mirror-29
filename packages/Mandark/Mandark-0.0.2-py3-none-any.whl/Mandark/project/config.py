# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base Configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'  # noqa
    # import binascii
    # import os
    # print(binascii.hexlify(os.urandom(24)))
    SECRET_KEY = "3833bffa12a864aaa90b8dda70d5c11694ab2ecfa3a99455"
    CSRF_ENABLED = True
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    SECURITY_PASSWORD_SALT = 'yH41YQQF5qbxZnYA'
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
