import pytest

from database import    (  
                            User, Chip, Location, 
                            DbI, UserI, ChipI, LocationI, 
                            Connector, ParamsUser, ParamsChip, ParamsLocation,
                            return_codes as retc
                        )
from .utils import FAKE_USERS, FAKE_CHIPS, fake_engine, fake_session


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

################################################################################
############################# USER RELATED TESTS ###############################
################################################################################

def test_create_user(clean_user_i: UserI):
    assert clean_user_i.create(FAKE_USERS[0].params) == (retc.DB_OK, dict(name=FAKE_USERS[0].name,
                                                                            email=FAKE_USERS[0].email, 
                                                                            id=None, 
                                                                            chip=None))



def test_create_user_duplicate(clean_user_i: UserI):
    def first(self):
        return FAKE_USERS[0].obj
    clean_user_i.session.first = first
    assert clean_user_i.create(FAKE_USERS[0].params) == (retc.EMAIL_ALREADY_REGISTERED, dict())


def test_get_user_by_id_no_user(clean_user_i: UserI):
    assert clean_user_i.get_by_id(_id=1) == (retc.NO_USER, dict())


def test_get_user_by_id(clean_user_i: UserI):
    def first(self):
        return FAKE_USERS[0].obj
    clean_user_i.session.first = first
    assert clean_user_i.get_by_id(_id=1) == (retc.DB_OK,
                                                dict(id=FAKE_USERS[0].id,
                                                    name=FAKE_USERS[0].name,
                                                    email=FAKE_USERS[0].email,
                                                    chip=FAKE_USERS[0].chip_iccid))


def test_get_all_users(clean_user_i: UserI):
    assert clean_user_i.get_all() == (retc.DB_OK, list())


################################################################################
############################# CHIP RELATED TESTS ###############################
################################################################################


def test_create_chip(clean_chip_i: ChipI):
    assert clean_chip_i.create(FAKE_CHIPS[0].params) == (retc.DB_OK, 
                                                            dict(iccid=FAKE_CHIPS[0].iccid, 
                                                                id=FAKE_CHIPS[0].id, 
                                                                user_id=FAKE_CHIPS[0].user_id))
    

def test_create_chip_duplicate(clean_chip_i: ChipI):
    def first(self):
        return FAKE_CHIPS[0].obj
    clean_chip_i.session.first = first
    assert clean_chip_i.create(FAKE_CHIPS[0].params) == (retc.CHIP_ALREADY_EXISTS, dict())



################################################################################
############################ LOCATION RELATED TESTS ############################
################################################################################
