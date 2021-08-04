from os import times
from sqlalchemy import create_engine
import traceback
from datetime import datetime

from database import User, Chip, Location, ParamsUser, ParamsChip, ParamsLocation

# mainly to run on RAM and preserve disk 
fake_engine = create_engine('sqlite+pysqlite:///:memory:', echo=False, future=True)


class fake_session():
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        traceback.print_exception(exc_type, exc_value, tb)
        return False

    def add(self, *args, **kwargs):
        pass

    def commit(self):
        pass

    def query(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def first(self, *args, **kwargs):
        pass

    def all(self, *args, **kwargs):
        return []


class FakeUser():
    def __init__(self, _name: str, _email: str, _id: int=None, _chip_iccid: str=None) -> None:
        self.name = _name
        self.email = _email
        self.id = _id
        self.chip_iccid = _chip_iccid
        self.obj = User(id=_id, name=_name, email=_email, chip=_chip_iccid)
        self.params = ParamsUser(name=_name, email=_email)


class FakeChip():
    def __init__(self, _iccid: str, _id: int=None, _user_id: int=None) -> None:
        self.id = _id
        self.iccid = _iccid
        self.user_id = _user_id
        self.obj = Chip(id=_id, iccid=_iccid, user_id=_user_id)
        self.params = ParamsChip(iccid=_iccid)


class FakeLocation():
    def __init__(self, _lat: float, _lon: float, _timestamp: datetime, _chip_iccid: str, _user_id: int=None, ) -> None:
        self.lat = _lat
        self.lon = _lon
        self.timestamp = _timestamp
        self.user_id = _user_id
        self.chip_iccid = _chip_iccid
        self.obj = Location(lat=_lat, lon=_lon, timestamp=_timestamp, user_id=_user_id)
        self.params = ParamsLocation()


FAKE_USERS = [
    FakeUser(_id=1, _name='John Titor', _email='john@email.com'),
    FakeUser(_name='Maria C. Dawn', _email='mcd@email.com'),
]

FAKE_CHIPS = [
    FakeChip(_iccid='1234567890'),
]

FAKE_LOCATIONS = [
    FakeLocation(_lat=-13.064, _lon=6.2343, _timestamp=1628110246, _chip_iccid='1234567890', _user_id=1),
]