from app import app
from app.utils.returns import Returns
from flask import request
from app.services.user import UserService
from app.utils.response import MakeResponse
from app.utils.authorization import Authorization

@app.route("/user/<int:id>", methods=['GET'])
@Authorization.token_required
def get_user(current_user, id):
    if id > 0:
        user = UserService.get(id)
        if user is not None:
            return MakeResponse.ok(object=user)
        return MakeResponse.not_found(user_message="The entered ID does not match any user.")
    return MakeResponse.bad_request(user_message="Please send a valid ID.")

@app.route("/user", methods=['POST'])
def insert_user():
    try:
        if UserService.create(request.get_json()) == True: 
            return MakeResponse.created()
        return MakeResponse.conflict(user_message="The sended object has values that conflict with the database's unique values.")
    except:
        return MakeResponse.bad_request(user_message="Please send a valid object.")

@app.route("/user/<id_or_email>", methods=['DELETE'])
@Authorization.token_required
def delete_user(current_user, id_or_email):
    if UserService.delete(id_or_email) == Returns.OK:
        return MakeResponse.ok()
    return MakeResponse.bad_request(user_message="The ID/e-mail entered does not match any user.")

@app.route("/user", methods=['PUT'])
@Authorization.token_required
def update_user(current_user):
    if UserService.update(request.get_json()) == Returns.CREATED:
        return MakeResponse.ok()
    return MakeResponse.bad_request("Please verify service arguments and try again.")

@app.route("/user", defaults={'page':None, 'max_per_page': None, 'excluded': 'false'}, methods=['GET'])
@Authorization.token_required
def list_all_users(current_user, page, max_per_page, excluded):
    try:
        return MakeResponse.ok(object = UserService.list_all(page, max_per_page, excluded))
    except:
        return MakeResponse.bad_request("Please verify service arguments and try again.")

@app.route("/user/login", methods=['POST'])
def login_user():
    try:
        key = UserService.login(request.get_json()['email'], request.get_json()['password'])
        return MakeResponse.ok(object=key, user_message="Welcome, " + UserService.get(key['email'])['name'] + "!")
    except:
        return MakeResponse.unauthorized("The username and/or password are incorrect.")