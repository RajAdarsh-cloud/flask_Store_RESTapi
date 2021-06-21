# from werkzeug.security import safe_str_cmp
from models.user import UserModel

# users = [
#     User(1,'bob', 'asdf'),
# ]
#
# username_mapping = {u.username: u for u in users}  # set comprehension
# userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    # user = username_mapping.get(username, None)  # additional benefit over ['']
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):  # specific to flask_jwt
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
