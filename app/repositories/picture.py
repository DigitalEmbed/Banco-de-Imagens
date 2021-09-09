from app.repositories.user import UserRepository
from app import db, app
from datetime import datetime
from app.models.picture import Picture
from app.utils.page import Page
from app.utils.returns import Returns
import base64
from os import path, makedirs
from PIL import Image
from io import BytesIO

class PictureRepository():
    @staticmethod
    def get(object):
        try:
            search_word = Picture.__to_search_word__(object)
            if type(search_word) == int:
                return Picture.__to_dict__(Picture.query.filter(Picture.id == search_word, Picture.excluded_at == None).one())
            elif type(search_word) ==  str:
                return Picture.__to_dict__(Picture.query.filter(Picture.label == search_word, Picture.excluded_at == None).one())
        except:
            return None

    @staticmethod
    def exists(object): 
        search_word = Picture.__to_search_word__(object)
        if search_word is not None and UserRepository.get(search_word) is not None:
            return True
        return False

    @staticmethod
    def save(object, data=None):
        try:
            dict = Picture.__to_dict__(object)
            if 'id' in dict and dict['id'] > 0:
                unique_verification = Picture.query.filter(Picture.label==dict['label'], Picture.excluded_at==None, Picture.id != dict['id']).first()
            else:
                unique_verification = Picture.query.filter(Picture.label==dict['label'], Picture.excluded_at==None).first()

            if unique_verification is not None:
                return Returns.INVALID_OBJECT

            if 'id' in dict:
                picture = Picture.query.get(dict['id'])
                picture.user_id = dict['user']['id']
                picture.label = dict['label']
                picture.updated_at = datetime.now()
                if 'excluded_at' in dict:
                    picture.excluded_at = dict['excluded_at']
            else:
                picture = Picture(dict['label'], dict['mime'], dict['user']['id'])

            if data is not None:
                directory = path.join(app.config['BASE_DIRECTORY'], dict['mime'])
                
                if path.exists(directory) == False:
                    makedirs(directory, exist_ok=True)
                format = str(dict['mime']).split("/")[1]
                file = open(directory + '/' + dict['label'] + '.' + format, 'wb')
                file.write(base64.b64decode(str(data)))
            
            db.session.add(picture)
            db.session.commit()
            return Returns.CREATED
        except:
            return Returns.INVALID_OBJECT 

    @staticmethod
    def delete(object):
        search_word = Picture.__to_search_word__(object)
        try:
            picture = PictureRepository.get(search_word)
            picture['excluded_at'] = datetime.now()
            if PictureRepository.save(picture) == Returns.CREATED:
                return Returns.OK
            return Returns.INVALID_OBJECT
        except:
            return Returns.NOT_FOUND
    
    @staticmethod
    def list_all(page=None, max_per_page=None, excluded='false'):
        if excluded == 'true':
            picture_list = Picture.query.filter_by().paginate(page=page, max_per_page=max_per_page)
        elif excluded == 'only':
            picture_list = Picture.query.filter_by(excluded_at=not None).paginate(page=page, max_per_page=max_per_page)
        else:
            picture_list = Picture.query.filter_by(excluded_at=None).paginate(page=page, max_per_page=max_per_page)
        return Page.to_dict(Picture, picture_list)

    @staticmethod
    def load(id_or_label, height=0, width=0, thumbnail=False):
        try:
            picture = PictureRepository.get(id_or_label)
            format = str(picture['mime']).split('/')[1]
            directory = path.join(app.config['BASE_DIRECTORY'], 'image', format)
            with Image.open(directory + '/' + picture['label'] + '.' + format) as file:
                buffer = BytesIO()
                if (height != 0 and width != 0):
                    file.thumbnail([height, width])
                file.save(buffer, "JPEG")
                return base64.b64encode(buffer.getvalue())
        except:
            return None