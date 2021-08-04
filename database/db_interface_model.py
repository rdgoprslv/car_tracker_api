from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple
from attr import dataclass
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker


class ConnectorInterface(ABC):
    @abstractmethod
    def __init__(self, session_maker: sessionmaker, _engine: Engine) -> None:
        pass


class DbInterface(ABC):
    @abstractmethod
    def __init__(self, connector: ConnectorInterface, auto_init: bool) -> None:
        pass

    @abstractmethod
    def create_db(self) -> None:
        pass
    
    @abstractmethod
    def delete_db(self) -> None:
        pass


class Params():
    pass


@dataclass
class ParamsUser(Params):
    name: str=None
    email: str=None


@dataclass
class ParamsChip(Params):
    iccid: str=None


@dataclass
class ParamsLocation(Params):
    lat: float=None
    lon: float=None
    timestamp: datetime=None
    user_id: int=None
    chip_iccid: str=None


class OperationsInterface(ABC):
    @abstractmethod
    def __init__(self, connector: ConnectorInterface) -> None:
        pass

    @abstractmethod
    def create(self, params: Params) -> Tuple[str, dict]:
        pass

    @abstractmethod
    def get_by_id(self, _id: int) -> Tuple[str, dict]:
        pass

    @abstractmethod
    def get(self, params: Params) -> Tuple[str, List[dict]]:
        pass

    @abstractmethod
    def get_all(self) -> Tuple[str, List[dict]]:
        pass

    @abstractmethod
    def delete(self, params: Params) -> Tuple[str, dict]:
        pass
    
    @abstractmethod
    def update(self, params: Params, _id: int) -> Tuple[str, dict]:
        pass


class UserInterface(OperationsInterface):
    pass


class ChipInterface(OperationsInterface):
    @abstractmethod
    def link_chip_to_user(self, chip_id: int, user_id: int) -> Tuple[str, dict]:
        pass


class LocationInterface(OperationsInterface):
    @abstractmethod
    def get_last_location(self, user_id: int) -> Tuple[str, str]:
        pass
