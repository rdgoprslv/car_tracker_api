from typing import List, Tuple
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from db_interface_model import DbInterface
from .models import *


class Db(DbInterface):
    def __init__(self, session_maker: sessionmaker) -> None:
        self.session = session_maker

    def create_user(name: str, email: str) -> Tuple(str, dict):
        pass

    def get_user(id: int) -> Tuple(str, dict):
        pass

    def get_all_users() -> Tuple(str, List[dict]):
        pass

    def create_chip(iccid: str) -> Tuple(str, dict):
        pass

    def get_chip_by_id(id: int) -> Tuple(str, dict):
        pass

    def get_chip_by_iccid(iccid: str) -> Tuple(str, dict):
        pass

    def link_chip_to_user(chip_id: int, user_id: int) -> Tuple(str, dict):
        pass

    def create_location(lat: float, lon: float, timestamp: datetime, user_id: int) -> Tuple(str, dict):
        pass

    def get_last_location(user_id: int) -> Tuple(str, str):
        pass

    def get_all_locations() -> Tuple(str, str):
        pass

    def get_all_locs_from_user(user_id: int) -> Tuple(str, str):
        pass





