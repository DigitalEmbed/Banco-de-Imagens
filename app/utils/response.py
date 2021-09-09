from flask import make_response, jsonify

class MakeResponse():
    @staticmethod
    def response(number, status, object=None, user_message=None):
        response = {"status":status}
        if object is not None:
            response['object'] = object
        if user_message is not None:
            response['user_message'] = str(user_message)
        return make_response(jsonify(response), number)

    @staticmethod
    def ok(object=None, user_message=None):
        return MakeResponse.response(200, "OK", object, user_message)
    
    @staticmethod
    def bad_request(user_message=None):
        return MakeResponse.response(400, "Bad request", None, user_message)

    @staticmethod
    def not_found(user_message=None):
        return MakeResponse.response(404, "Object not found", None, user_message)
    
    @staticmethod
    def created(user_message=None):
        return MakeResponse.response(201, "Created", None, user_message)

    @staticmethod
    def conflict(user_message=None):
        return MakeResponse.response(409, "Conflict", None, user_message)

    @staticmethod
    def unauthorized(user_message=None):
        return MakeResponse.response(401, "Unauthorized", None, user_message)