from werkzeug.security import safe_str_cmp
from user import UserModel

def authenticate(username, password):
    '''
    authenicate method for JWT
    returns user if user exists in DB
    '''
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    '''
    identity method for JWT
    returns user_id from DB
    '''
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
