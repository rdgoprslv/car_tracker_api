from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple


class DbInterface(ABC):
    @abstractmethod
    def create_user(name: str, email: str) -> Tuple(str, dict):
        pass

    @abstractmethod
    def get_user(id: int) -> Tuple(str, dict):
        pass

    @abstractmethod
    def get_all_users() -> Tuple(str, List[dict]):
        pass

    @abstractmethod
    def create_chip(iccid: str) -> Tuple(str, dict):
        pass

    @abstractmethod
    def get_chip_by_id(id: int) -> Tuple(str, dict):
        pass

    @abstractmethod
    def get_chip_by_iccid(iccid: str) -> Tuple(str, dict):
        pass

    @abstractmethod
    def link_chip_to_user(chip_id: int, user_id: int) -> Tuple(str, dict):
        pass

    @abstractmethod
    def create_location(lat: float, lon: float, timestamp: datetime, user_id: int) -> Tuple(str, dict):
        pass

    @abstractmethod
    def get_last_location(user_id: int) -> Tuple(str, str):
        pass

    @abstractmethod
    def get_all_locations() -> Tuple(str, str):
        pass

    @abstractmethod
    def get_all_locs_from_user(user_id: int) -> Tuple(str, str):
        pass
    