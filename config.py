"""
Application configurations.
"""

from os import getenv

# pylint:disable=too-few-public-methods, invalid-name


class Config(object):
    """
    Base configuration.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('APP_SECRET_KEY')


class TestingConfig(Config):
    """
    Configuration for testing environment.
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv('TESTING_DATABASE_URI')


class DevelopmentConfig(Config):
    """
    Configuration for development environment.
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = getenv('DEVELOPMENT_DATABASE_URI')


configurations = {
    "testing": TestingConfig,
    "development": DevelopmentConfig
}
