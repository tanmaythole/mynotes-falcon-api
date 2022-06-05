import falcon
from db.models.UserModel import Users
from sqlobject import *
from utils.auth import check_password, hash_password



class UserStorage:
    def create_user(self, username, password):
        """
        Create user and store in db
        """
        # check whether user already exist or not
        is_exist = list(Users.select(Users.q.username==username))

        if len(is_exist)>0:
            raise falcon.HTTPBadRequest(title="Username Already Exist!")

        try:
            user = Users(username=username, password=hash_password(password).decode('utf-8'))
            return user.get_dict()
        except Exception as e:
            raise falcon.HTTPBadRequest(title=str(e))
        
    @staticmethod
    def get_user(username, password):
        user = Users.select(Users.q.username == username)
        if check_password(password, user[0].password):
            return user
        else:
            return None