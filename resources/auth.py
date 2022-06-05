import json
import falcon
import jwt
from db.storage.UserStorage import UserStorage


class Auth:
    """
    Authentication API
    """
    def login(self, req, resp):
        """
        Login
        """
        data = json.loads(req.stream.read())
        self._authenticate(
            data.get('username'),
            data.get('password'),
            req, 
            resp
        )

    def register(self, req, resp):
        """
        Register a user
        """
        data = json.loads(req.stream.read())
        
        if not data.get('username') or not data.get('password'):
            resp.status = 400
            resp.media = {
                "error": "Username and password are required!"
            }
        else:
            user = UserStorage().create_user(data.get('username'), data.get('password'))
            resp.status = falcon.HTTP_201
            resp.media = user
    
    def _authenticate(self, username, password, req, resp):
        """
        Authenticate user and generate jwt token
        """
        if not username or not password:
            raise falcon.HTTPBadRequest("Bad Request", "Please enter valid username and password")
        else:
            user = UserStorage.get_user(username, password)
            if user.count()>0:
                user = user[0].get_dict()
                payload = {
                    "user": user['id']
                }
                secret = "secret"
                algo = "HS256"
                token = jwt.encode(payload=payload, key=secret, algorithm=algo)
                user['token'] = token
                resp.media = user
                resp.status = 200

    def on_post(self, req, resp):
        """
        POST request for auth
        """
        if req.path=='/api/auth/login/':
            self.login(req, resp)
        elif req.path=='/api/auth/register/':
            self.register(req, resp)
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                "error": "API Not Found!"
            }