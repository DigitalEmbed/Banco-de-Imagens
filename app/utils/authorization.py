from app.services.user import UserService
from app.utils.response import MakeResponse
from functools import wraps
from app import app
from flask import request
from jwt import decode

class Authorization:
    @staticmethod
    def token_required(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token is None:
                return MakeResponse.unauthorized(user_message="Token required.")

            token = token.split(' ')
            if (token[0] != 'Bearer'):
                return MakeResponse.unauthorized(user_message="Invalid token format.")
                        
            try:
                decoded_token = decode(token[1], app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = UserService.get(decoded_token['email'])
            except:
                return MakeResponse.unauthorized(user_message="Invalid or expired token.")
            
            return function(current_user, *args, **kwargs)
        return decorated