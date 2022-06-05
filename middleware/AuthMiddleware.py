import jwt
import falcon
from sqlobject import *
from db.models.UserModel import Users

class AuthMiddleware:
    """
    Authentication Middelware
    """
    def process_request(self, req, resp):
        if '/login' in req.path or '/register' in req.path:
            return
        
        token = req.get_header('Authorization')

        if token is None:
            raise falcon.HTTPUnauthorized(
                'Auth Token Required!', 
                "Please provide login credentials to continue the request."
            )

        user = self._decrypt_token(token)
        if not user:
            raise falcon.HTTPUnauthorized(
                "Invalid Token", 
                "The provided auth token is not valid. Please request a new token and try again."
            )
        else:
            # store current user in req
            req.context['current_user'] = user


    def _decrypt_token(self, token):
        """
        Decrypt the jwt token
        """
        try:
            payload = jwt.decode(token, "secret", algorithms="HS256")
            user = Users.get(payload['user']).get_dict()
            return user
        except (jwt.DecodeError, jwt.ExpiredSignatureError, SQLObjectNotFound) as e:
            print(str(e))
            return False