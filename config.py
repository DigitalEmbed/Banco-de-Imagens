import os.path
import string
import random

__basedir__ = os.path.abspath(os.path.dirname(__file__))
__random_str__ = string.ascii_letters + string.digits + string.ascii_uppercase
__key__ = ''.join(random.choice(__random_str__) for index in range(50))

DEBUG = True

BASE_DIRECTORY = __basedir__
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(__basedir__, 'storage.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = __key__