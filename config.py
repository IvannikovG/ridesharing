import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgres://rnforvzzltqhju:3db84efc383bef98cb6933c27e9a77006f330292451916d8adac0a43d3379ae6@ec2-34-233-226-84.compute-1.amazonaws.com:5432/d6soqquhdtkgd0'
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RIDES_PER_PAGE = 5
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    LANGUAGES = ['en', 'ru']
