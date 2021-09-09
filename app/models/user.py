from app import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    updated_at = db.Column(db.DateTime, default=None)
    excluded_at = db.Column(db.DateTime, default=None)

    def __init__(
        self, 
        name, 
        email, 
        password
    ):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def __check__(object):
        if type(object) == User and object.id >= 0:
            return True
        if(
            object is not None and 
            all(key in object for key in ('name', 'email'))
        ):
            if ('id' in object and (type(object['id']) != int or object['id'] <= 0)):
                return False
            return True
        return False

    @staticmethod
    def __to_dict__(object):
        if User.__check__(object) == True:
            if type(object) == User:
                user = {}
                user['name'] = str(object.__getattribute__('name'))
                user['email'] = object.__getattribute__('email')
                user['password'] = str(object.__getattribute__('password'))
                if (object.__getattribute__('id') > 0):
                    user['id'] = object.__getattribute__('id')
                if (object.__getattribute__('updated_at') is not None):
                    user['updated_at'] = object.__getattribute__('updated_at')
                if (object.__getattribute__('excluded_at') is not None):
                    user['excluded_at'] = object.__getattribute__('excluded_at')
                return user
            return object
        return None

    @staticmethod
    def __to_object__(dict):
        if User.__check__(dict) == True:
            if type(dict) != User:
                user = User(
                    name = dict['name'],
                    email = dict['email'],
                    password = dict['password']
                )
                if 'id' in dict and dict['id'] > 0:
                    user.id = int(dict['id'])
                if 'excluded_at' in dict:
                    user.excluded_at = dict['excluded_at']
                if 'updated_at' in dict:
                    user.updated_at = dict['updated_at']
                return user
            return dict
        return None

    @staticmethod
    def __to_search_word__(object):
        if type(object) == int:
            return int(object)
        elif type(object) == str:
            if object.isdigit() == True:
                return int(object)
            return object
        else:
            try:
                return User.__to_object__(object).id
            except:
                return None