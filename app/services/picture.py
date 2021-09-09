from app.repositories.picture import PictureRepository

class PictureService():
    @staticmethod
    def get(id_or_label):
        return PictureRepository.get(id_or_label)

    @staticmethod
    def create(picture, data):
        return PictureRepository.save(picture, data)

    @staticmethod
    def delete(id_or_label):
        return PictureRepository.delete(id_or_label)

    @staticmethod
    def update(picture, data):
        return PictureRepository.save(picture, data)

    @staticmethod
    def list_all(page=None, max_per_page=None, excluded='false'):
        return PictureRepository.list_all(page, max_per_page, excluded)

    @staticmethod
    def load(id_or_label, height=0, width=0):
        return PictureRepository.load(id_or_label, height, width)