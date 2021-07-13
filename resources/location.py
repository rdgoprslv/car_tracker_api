import json

import falcon
from database import Session, Chip, User, Location
from datetime import datetime


class LocationResource():
    def on_post(self, req, resp):
        data = req.get_media()
        # data validation?
        with Session() as session:
            chip = session.query(Chip).filter(Chip.iccid==data['id']).first()
            if chip is None:
                raise falcon.HTTPBadRequest(description="Invalid ICCID.")
            location = Location(
                lat=data['lat'],
                lon=data['lon'],
                timestamp=datetime.fromtimestamp(data['timestamp']),
                user_id=chip.user_id
            )
            session.add(location)
            session.commit()
            resp.text = repr(location)

    def on_get(self, req, resp):
        with Session() as session:
            locs = session.query(Location).all()
            resp.text = repr(locs)

    def on_get_last(self, req, resp, user_id):
        with Session() as session:
            location = session.query(Location).filter(Location.user_id == user_id).order_by(Location.timestamp.desc()).first()
            if location is None:
                raise falcon.HTTPBadRequest(description="This user didn't send any location yet.")
            resp.text = json.dumps({'link': location.get_maps_search_link()})

    def on_get_user_all(self, req, resp, user_id):
        with Session() as session:
            locations = session.query(Location).filter(Location.user_id == user_id).order_by(Location.timestamp.desc()).all()
            if not len(locations):
                raise falcon.HTTPBadRequest(description="This user didn't send any location yet.")
            resp.text = repr(locations)
