import falcon
from middleware.AuthMiddleware import AuthMiddleware
from resources import Notes, Auth

def get_app():
    """
    Falcon app
    """
    application = falcon.App()

    application.add_middleware(AuthMiddleware())

    application.add_route('/api/notes/', Notes())
    application.add_route('/api/notes/{note_id:int}', Notes(), suffix="note")
    application.add_route('/api/auth/login/', Auth())
    application.add_route('/api/auth/register/', Auth())

    return application