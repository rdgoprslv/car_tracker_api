from random import randint
import pytest
from faker import Faker

from database import (Chip, ChipI, Connector, DbI, Location, LocationI,
                      ParamsChip, ParamsLocation, ParamsUser, User, UserI,
                      return_codes as retc)

from .utils import (fake_engine, fake_session, get_fake_chip,
                    get_fake_location, get_fake_user, randid)

fake = Faker()


@pytest.fixture()
def clean_connector():
    class mock_session(fake_session):
        pass
    connector = Connector(session_maker=mock_session, _engine=fake_engine)
    yield connector
    del connector


@pytest.fixture()
def clean_db(clean_connector: Connector):
    db = DbI(clean_connector, auto_init=False)
    db.delete_db()
    db.create_db()
    yield db
    del db


@pytest.fixture()
def clean_user_i(clean_connector: Connector):
    user_i = UserI(clean_connector)
    yield user_i
    del user_i


@pytest.fixture()
def clean_chip_i(clean_connector: Connector):
    chip_i = ChipI(clean_connector)
    yield chip_i
    del chip_i


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['pt_BR']


@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return 'DEADBEEF'


################################################################################
############################# USER RELATED TESTS ###############################
################################################################################

def test_create_user(clean_user_i: UserI, faker):
    fuser = get_fake_user(faker)
    assert clean_user_i.create(fuser.params) == (retc.DB_OK, dict(  id=None,
                                                                    name=fuser.name,
                                                                    email=fuser.email,
                                                                    chip=None))


def test_create_user_duplicate(clean_user_i: UserI, faker):
    fuser = get_fake_user(faker)
    def first(self):
        return fuser.obj
    clean_user_i.session.first = first
    assert clean_user_i.create(fuser.params) == (retc.EMAIL_ALREADY_REGISTERED, dict())


def test_get_user_by_id_no_user(clean_user_i: UserI):
    assert clean_user_i.get_by_id(_id=1) == (retc.NO_USER_WITH_ID, dict())


def test_get_user_by_id(clean_user_i: UserI, faker):
    fuser = get_fake_user(faker)
    def first(self):
        return fuser.obj
    clean_user_i.session.first = first
    assert clean_user_i.get_by_id(_id=1) == (retc.DB_OK, dict(  id=fuser.id,
                                                                name=fuser.name,
                                                                email=fuser.email,
                                                                chip=fuser.chip_iccid))


def test_get_all_users(clean_user_i: UserI):
    assert clean_user_i.get_all() == (retc.DB_OK, list())


################################################################################
############################# CHIP RELATED TESTS ###############################
################################################################################


def test_create_chip(clean_chip_i: ChipI, faker):
    fchip = get_fake_chip(faker)
    assert clean_chip_i.create(fchip.params) == (retc.DB_OK, dict(  iccid=fchip.iccid,
                                                                    id=None,
                                                                    user_id=fchip.user_id))


def test_create_chip_duplicate(clean_chip_i: ChipI, faker):
    fchip = get_fake_chip(faker)
    def first(self):
        return fchip.obj
    clean_chip_i.session.first = first
    assert clean_chip_i.create(fchip.params) == (retc.CHIP_ALREADY_EXISTS, dict())


def test_get_chip_by_id_no_chip(clean_chip_i: ChipI):
    assert clean_chip_i.get_by_id(_id=1) == (retc.NO_CHIP_WITH_ID, dict())


def test_get_chip_by_id(clean_chip_i: ChipI, faker):
    fchip = get_fake_chip(faker)
    def first(self):
        return fchip.obj
    clean_chip_i.session.first = first
    assert clean_chip_i.get_by_id(_id=fchip.id) == (retc.DB_OK, dict(   iccid=fchip.iccid,
                                                                        id=fchip.id,
                                                                        user_id=fchip.user_id))


def test_get_all_chips(clean_chip_i: ChipI):
    assert clean_chip_i.get_all() == (retc.DB_OK, list())


def test_link_chip_to_user_no_user(clean_chip_i: ChipI, faker):
    fchip = get_fake_chip(faker)
    def first(self):
        self.i+=1
        return self.items[self.i-1]
    clean_chip_i.session.i = 0
    clean_chip_i.session.items = (None, fchip.obj)
    clean_chip_i.session.first = first
    assert clean_chip_i.link_chip_to_user(chip_id=fchip.id, user_id=1) == (retc.NO_USER_WITH_ID, dict())


def test_link_chip_to_user_no_chip(clean_chip_i: ChipI, faker):
    fuser = get_fake_user(faker)
    def first(self):
        self.i+=1
        return self.items[self.i-1]
    clean_chip_i.session.i = 0
    clean_chip_i.session.items = (fuser.obj, None)
    clean_chip_i.session.first = first
    assert clean_chip_i.link_chip_to_user(chip_id=1, user_id=fuser.id) == (retc.NO_CHIP_WITH_ID, dict())


def test_link_chip_to_user(clean_chip_i: ChipI, faker):
    fchip = get_fake_chip(faker)
    fuser = get_fake_user(faker)
    def first(self):
        self.i+=1
        return self.items[self.i-1]
    clean_chip_i.session.i = 0
    clean_chip_i.session.items = (fuser.obj, fchip.obj)
    clean_chip_i.session.first = first
    status, data = clean_chip_i.link_chip_to_user(chip_id=fchip.id, user_id=fuser.id)
    assert status == retc.DB_OK
    assert data['id'] == fuser.id
    assert data['name'] == fuser.name
    assert data['email'] == fuser.email
    assert data['chip']['iccid'] == fchip.iccid
    assert data['chip']['id'] == fchip.id


################################################################################
############################ LOCATION RELATED TESTS ############################
################################################################################
