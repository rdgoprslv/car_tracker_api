import json

import falcon
from database import Session, User


class UserResource():
    def on_post(self, req:falcon.Request, resp):
        if 'email' not in req.media or 'name' not in req.media:
            raise falcon.HTTPBadRequest(description="Not enough parameters")

        media = req.get_media()
        user_email = media.get('email')
        user_name = media.get('name')

        with Session() as session:
            user = User(name=user_name, email=user_email)
            session.add(user)
            session.commit()
            resp.text = json.dumps({'user': repr(user)})

    def on_get(self, req, resp):
        with Session() as session:
            users = session.query(User).all()
            resp.text = json.dumps({'users': [repr(u) for u in users]})
