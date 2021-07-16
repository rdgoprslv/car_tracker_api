import falcon
from database import Session, User
from .utils import validate_dict
from database.return_codes import *


class UserResource():
    def on_post(self, req, resp):
        if not validate_dict(['email',  'name'], req.media):
            raise falcon.HTTPBadRequest(description=MISSING_PARAMETERS)

        with Session() as session:
            user = session.query(User).filter(User.email==req.media['email']).first()
            if user is not None:
                raise falcon.HTTPBadRequest(description=USER_ALREADY_REGISTERED)
            user = User(name=req.media['name'], email=req.media['email'])
            session.add(user)
            session.commit()
            resp.text = repr(user)
    def on_get(self, req, resp):
        with Session() as session:
            users = session.query(User).all()
            resp.text = repr(users)

    def on_get_single(self, req, resp, user_id):
        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                raise falcon.HTTPBadRequest(description="User doesn't exist")
            resp.text = repr(user)
