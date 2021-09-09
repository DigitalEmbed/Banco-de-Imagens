from app.repositories.user import UserRepository

class UserService():

    @staticmethod
    def get(id_or_email):
        return UserRepository.get(id_or_email)

    @staticmethod
    def create(user):
        return UserRepository.save(user)

    @staticmethod
    def delete(id_or_email):
        return UserRepository.delete(id_or_email)

    @staticmethod
    def update(user):
        return UserRepository.save(user)

    @staticmethod
    def list_all(page=None, max_per_page=None, excluded='false'):
        return UserRepository.list_all(page, max_per_page, excluded)

    @staticmethod
    def login(email, password):
        return UserRepository.login(email, password)