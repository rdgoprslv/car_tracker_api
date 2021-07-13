import falcon
from database import Session, Chip, User


class ChipResource():
    def on_post(self, req, resp):
        if 'iccid' not in req.media:
            raise falcon.HTTPBadRequest(description="Not enough parameters")

        media = req.get_media()
        chip_iccid = media.get('iccid')

        with Session() as session:
            chip = session.query(Chip).filter(Chip.iccid==chip_iccid).first()
            if chip is not None:
                raise falcon.HTTPBadRequest(description="A chip with this ICCID already exists")
            chip = Chip(iccid=chip_iccid)
            session.add(chip)
            session.commit()
            resp.text = repr(chip)

    def on_get(self, req, resp):
        with Session() as session:
            chips = session.query(Chip).all()
            resp.text = repr(chips)

    def on_get_single(self, req, resp, chip_id):
        with Session() as session:
            chip = session.query(Chip).filter(Chip.id == chip_id).first()
            if chip is None:
                raise falcon.HTTPBadRequest(description="Chip doesn't exist")
            resp.text = repr(chip)

    def on_patch(self, req, resp):
        if 'chip_id' not in req.media or 'user_id' not in req.media:
            raise falcon.HTTPBadRequest(description="Not enough parameters")

        media = req.get_media()
        chip_id = media.get('chip_id')
        user_id = media.get('user_id')

        with Session() as session:
            user = session.query(User).filter(User.id==user_id).first()
            chip = session.query(Chip).filter(Chip.id==chip_id).first()
            if user is None or chip is None:
                raise falcon.HTTPBadRequest(description=f"User={user or None}, Chip={chip or None}")

            user.chip = chip
            chip.user = user
            session.commit()
            resp.text = repr(user)
