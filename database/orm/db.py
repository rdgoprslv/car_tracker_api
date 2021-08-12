from datetime import datetime
from typing import List, Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import and_

from database import database_url
from ..db_interface_model import *
from ..return_codes import *
from .models import *


engine = create_engine(database_url, echo=False, future=True)
Session = sessionmaker(engine, autocommit=False)


class Connector(ConnectorInterface):
    def __init__(self, session_maker: sessionmaker=Session, _engine: Engine=engine) -> None:     
        self.session = session_maker
        self.engine = _engine


_connector = Connector()


class DbI(DbInterface):
    def __init__(self, connector: Connector=_connector, auto_init: bool=True) -> None:
        self.connector = connector

        if auto_init:
            self.create_db()

    def create_db(self):
        mapper_registry.metadata.create_all(self.connector.engine)

    def delete_db(self):
        mapper_registry.metadata.drop_all(bind=self.connector.engine)


class UserI(UserInterface):
    def __init__(self, connector: Connector=_connector) -> None:
        self.session = connector.session

    def create(self, params: ParamsUser) -> Tuple[str, dict]:
        with self.session() as session:
            user = session.query(User).filter(User.email==params.email).first()
            if user is not None:
                return (EMAIL_ALREADY_REGISTERED, dict())
            user = User(name=params.name, email=params.email)
            session.add(user)
            session.commit()
            return (DB_OK, user.as_dict())

    def get_by_id(self, _id: int) -> Tuple[str, dict]:
        with self.session() as session:
            user = session.query(User).filter(User.id == _id).first()
            if user is None:
                return (NO_USER_WITH_ID, dict())
            return (DB_OK, user.as_dict())

    def get(self, params: ParamsUser) -> Tuple[str, List[dict]]:
        conditions = list()
        if params.name is not None:
            conditions.append(User.name==params.name)
        if params.email is not None:
            conditions.append(User.email==params.email)
        
        with self.session() as session:
            users = session.query(User).filter(and_(*conditions)).all()
            return (DB_OK, [u.as_dict() for u in users])

    def get_all(self) -> Tuple[str, List[dict]]:
        with self.session() as session:
            users = session.query(User).all()
            return (DB_OK, [u.as_dict() for u in users])

    def delete(self, params: ParamsUser) -> Tuple[str, dict]:
        pass
    
    def update(self, params: ParamsUser, _id: int) -> Tuple[str, dict]:
        pass


class ChipI(ChipInterface):
    def __init__(self, connector: Connector=_connector) -> None:
        self.session = connector.session

    def create(self, params: ParamsChip) -> Tuple[str, dict]:
        with self.session() as session:
            chip = session.query(Chip).filter(Chip.iccid==params.iccid).first()
            if chip is not None:
                return (CHIP_ALREADY_EXISTS, dict())
            chip = Chip(iccid=params.iccid)
            session.add(chip)
            session.commit()
            return (DB_OK, chip.as_dict())

    def get_by_id(self, _id: int) -> Tuple[str, dict]:
        with self.session() as session:
            chip = session.query(Chip).filter(Chip.id == _id).first()
            if chip is None:
                return (NO_CHIP_WITH_ID, dict())
            return (DB_OK, chip.as_dict())

    def get(self, params: ParamsChip) -> Tuple[str, dict]:
        pass

    def get_all(self) -> Tuple[str, List[dict]]:
        with self.session() as session:
            chips = session.query(Chip).all()
            return (DB_OK, [c.as_dict() for c in chips])

    def delete(self, params: ParamsChip) -> Tuple[str, dict]:
        pass
    
    def update(self, params: ParamsChip, _id: int) -> Tuple[str, dict]:
        pass

    def link_chip_to_user(self, chip_id: int, user_id: int) -> Tuple[str, dict]:
        with self.session() as session:
            user = session.query(User).filter(User.id==user_id).first()
            chip = session.query(Chip).filter(Chip.id==chip_id).first()
            if user is None or chip is None:
                description = NO_USER_WITH_ID if user is None else NO_CHIP_WITH_ID
                return (description, dict())
            user.chip = chip
            chip.user = user
            session.commit()
            return (DB_OK, user.as_dict())


class LocationI(LocationInterface):
    def __init__(self, connector: Connector=_connector) -> None:
        self.session = connector.session

    def create_location(self, lat: float, lon: float, timestamp: datetime, user_id: int) -> Tuple[str, dict]:
        pass

    def get_last_location(self, user_id: int) -> Tuple[str, str]:
        pass

    def get_all_locations(self) -> Tuple[str, List[dict]]:
        pass

    def get_all_locs_from_user(self, user_id: int) -> Tuple[str, str]:
        pass
