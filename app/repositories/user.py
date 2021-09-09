from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from app import app, db
from jwt import encode
from datetime import datetime
from app.models.user import User
from app.utils.page import Page
from app.utils.returns import Returns

class UserRepository():
    @staticmethod
    def get(object):
        try:
            search_word = User.__to_search_word__(object)
            if type(search_word) == int:
                return User.__to_dict__(User.query.filter_by(id = search_word, excluded_at=None).one())
            elif type(search_word) ==  str:
                return User.__to_dict__(User.query.filter_by(email = search_word, excluded_at=None).one())
        except:
            return None

    @staticmethod
    def exists(object): 
        search_word = User.__to_search_word__(object)
        if search_word is not None and UserRepository.get(search_word) is not None:
            return True
        return False

    @staticmethod
    def save(object):
        try:
            dict = User.__to_dict__(object)
            if 'id' in dict and dict['id'] > 0:
                unique_verification = User.query.filter(User.email==dict['email'], User.excluded_at==None, User.id != dict['id']).first()
            else:
                unique_verification = User.query.filter(User.email==dict['email'], User.excluded_at==None).first()
            
            if unique_verification is not None:
                return Returns.INVALID_OBJECT

            if 'id' in dict:
                user = User.query.get(dict['id'])
                user.name = dict['name']
                user.email = dict['email']
                user.updated_at = datetime.now()
                user.password = generate_password_hash(dict['password'])
                if 'excluded_at' in dict:
                    user.excluded_at = dict['excluded_at']
            else:
                user = User(dict['name'], dict['email'], dict['password'])
            
            db.session.add(user)
            db.session.commit()
            return Returns.CREATED
        except:
            return Returns.INVALID_OBJECT 

    @staticmethod
    def delete(object):
        search_word = User.__to_search_word__(object)
        try:
            user = UserRepository.get(search_word)
            user['excluded_at'] = datetime.now()
            UserRepository.save(user)
            return Returns.OK
        except:
            return Returns.NOT_FOUND
    
    @staticmethod
    def list_all(page=None, max_per_page=None, excluded='false'):
        if excluded == 'true':
            user_list = User.query.filter_by().paginate(page=page, max_per_page=max_per_page)
        elif excluded == 'only':
            user_list = User.query.filter_by(excluded_at=not None).paginate(page=page, max_per_page=max_per_page)
        else:
            user_list = User.query.filter_by(excluded_at=None).paginate(page=page, max_per_page=max_per_page)
        return Page.to_dict(User, user_list)

    @staticmethod
    def login(email, password):
        user = UserRepository.get(email)
        if check_password_hash(user['password'], password) == True:
            expiration_date = datetime.now() + timedelta(hours=12)
            token = encode({'email': user['email'], 'exp': expiration_date}, app.config['SECRET_KEY'], algorithm="HS256")
            key = {
                'email': user['email'],
                'expiration_date': expiration_date,
                'token': token
            }
            return key
        return None