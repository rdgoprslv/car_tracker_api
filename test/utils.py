from sqlalchemy import create_engine
import traceback
from datetime import datetime
from random import randint

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


def get_fake_user(faker, chip_iccid: str=None):
    return FakeUser(_name=faker.name(), _email=faker.email(), _id=randid(), _chip_iccid=chip_iccid or None)


def get_fake_chip(faker, user_id: int=None):
    return FakeChip(_iccid=faker.bothify(text='####################'), _id=randid(), _user_id=user_id or None)


def get_fake_location(faker, chip_iccid: str=None, user_id: int=None):
    return FakeLocation(_lat=faker.latitude(),
                        _lon=faker.longitude(),
                        _timestamp=datetime.timestamp(faker.past_datetime()),
                        _chip_iccid=chip_iccid or faker.bothify(text='####################'),
                        _user_id=user_id or randid())


def randid():
    return randint(0, 10000000)
