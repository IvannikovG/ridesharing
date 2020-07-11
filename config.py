import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgres://pkbkyxpxrlsozi:7e1b8c52b61373510a3a69cfb5fc574df6e6075425a6405027903d650a232430@ec2-52-0-155-79.compute-1.amazonaws.com:5432/daqndpqd8r4l4j"
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
