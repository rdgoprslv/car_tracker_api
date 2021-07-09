from wsgiref.simple_server import make_server
import falcon

from resources import *
from database import create_db

def create_app():
    app = falcon.App()
    app.add_route('/user', UserResource())
    app.add_route('/user/{user_id}', UserResource(), suffix="single")
    app.add_route('/chip', ChipResource())
    app.add_route('/chip/{chip_id}', ChipResource(), suffix="single")

    create_db()

    httpd = make_server('', 9000, app)
    httpd.serve_forever()

if __name__ == "__main__":
    create_app()
