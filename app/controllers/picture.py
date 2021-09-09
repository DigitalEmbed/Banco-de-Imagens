from app import app
from app.utils.returns import Returns
from flask import request
from app.utils.response import MakeResponse
from app.utils.authorization import Authorization
from app.services.picture import PictureService

@app.route("/picture/download", methods = ['POST'])
@Authorization.token_required
def download_picture(current_user):
    try:
        picture = PictureService.get(str(request.get_json()["label"]))
        picture["format"] = "base64"
        
        if 'height' in request.get_json() and 'width' in request.get_json():
            picture["data"] = str(PictureService.load(request.get_json()["label"], height=request.get_json()["height"], width=request.get_json()["width"]))
        else:
            picture["data"] = str(PictureService.load(request.get_json()["label"]))
        return MakeResponse.ok(object=picture)
    except:
        return MakeResponse.not_found()

@app.route("/picture", methods=['POST'])
@Authorization.token_required
def upload_picture(current_user):
    try:
        request.get_json()['user'] = current_user
        if PictureService.create(request.get_json(), request.get_json()['data']) == True:
            return MakeResponse.created()
        return MakeResponse.conflict(user_message="The sended object has values that conflict with the database's unique values.")
    except:
        return MakeResponse.bad_request(user_message="Please send a valid object.")

@app.route("/picture/<label>", methods=['DELETE'])
@Authorization.token_required
def delete_picture(current_user, label):
    request.get_json()['user'] = current_user
    if PictureService.delete(label) == Returns.OK:
        return MakeResponse.ok()
    return MakeResponse.bad_request(user_message="The label entered does not match any object.")

@app.route("/picture", methods=['PUT'])
@Authorization.token_required
def update_picture(current_user):
    if ('id' not in request.get_json()):
        return MakeResponse.bad_request("Please send picture ID.")
    request.get_json()['user'] = current_user
    if PictureService.update(request.get_json(), request.get_json()['data']) == Returns.CREATED:
        return MakeResponse.ok()
    return MakeResponse.bad_request("Please verify service arguments and try again.")

@app.route("/picture", defaults={'page':None, 'max_per_page': None, 'excluded': 'false'}, methods=['GET'])
@Authorization.token_required
def list_all_pictures(current_user, page, max_per_page, excluded):
    try:
        return MakeResponse.ok(object = PictureService.list_all(page, max_per_page, excluded))
    except:
        return MakeResponse.bad_request("Please verify service arguments and try again.")
    