from app import db
from datetime import datetime
from app.models.user import User
class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    label = db.Column(db.Integer, nullable=False)
    mime = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=None)
    excluded_at = db.Column(db.DateTime, default=None)

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(
        self,
        label,
        mime,
        user_id
    ):
        self.label = label
        self.user_id = user_id
        self.mime = mime

    def __repr__(self):
        return '<Picture %r>' % self.label

    @staticmethod
    def __check__(object):
        if type(object) == Picture and object.id >= 0:
            return True
        if(
            object is not None and 
            all(key in object for key in ('label', 'mime', 'user'))
        ):
            try:
                if User.query.get(object['user']['id']).id > 0:
                    return True
                print("2")
                return False
            except:
                try:
                    if User.query.get(object['user_id']).id > 0:
                        return True
                    return False
                except:
                    return False
        return False

    @staticmethod
    def __to_dict__(object):
        if Picture.__check__(object) == True:
            if type(object) == Picture:
                picture = {}
                picture['label'] = str(object.__getattribute__('label'))
                picture['mime'] = object.__getattribute__('mime')
                picture['user'] = User.__to_dict__(object.__getattribute__('user'))
                picture['uploaded_at'] = object.__getattribute__('uploaded_at')
                if (object.__getattribute__('id') > 0):
                    picture['id'] = object.__getattribute__('id')
                if (object.__getattribute__('updated_at') is not None):
                    picture['updated_at'] = object.__getattribute__('updated_at')
                if (object.__getattribute__('excluded_at') is not None):
                    picture['excluded_at'] = object.__getattribute__('excluded_at')
                return picture
            return object
        return None

    @staticmethod
    def __to_object__(dict):
        if Picture.__check__(dict) == True:
            if type(dict) != Picture:
                picture = Picture(
                    label = dict['label'],
                    mime = dict['mime'],
                    user_id = dict['user']['id'],
                    uploaded_at = dict['uploaded_at']
                )
                if 'id' in dict and dict['id'] > 0:
                    picture.id = int(dict['id'])
                if 'excluded_at' in dict:
                    picture.excluded_at = dict['excluded_at']
                if 'updated_at' in dict:
                    picture.updated_at = dict['updated_at']
                return picture
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
                return Picture.__to_object__(object).id
            except:
                return None