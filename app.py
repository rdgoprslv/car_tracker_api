from wsgiref.simple_server import make_server
import falcon

from resources import *
from database import DbI, UserI, ChipI, LocationI


def get_app():
    app = falcon.App()

    userR = UserResource(UserI())
    app.add_route('/user', userR)
    app.add_route('/user/{user_id}', userR, suffix="single")

    chipR = ChipResource(ChipI())
    app.add_route('/chip', chipR)
    app.add_route('/chip/{chip_id}', chipR, suffix="single")

    locationR = LocationResource(LocationI())
    app.add_route('/location', locationR)
    app.add_route('/location/{user_id}/last', locationR, suffix="last")
    app.add_route('/location/{user_id}/all', locationR, suffix="user_all")

    return app


def serve(app):
    httpd = make_server('', 9000, app)
    httpd.serve_forever()


def main():
    DbI()
    serve(get_app())


if __name__ == "__main__":
    main()
