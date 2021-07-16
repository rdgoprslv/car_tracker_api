
from typing import Iterable


def validate_dict(required_keys: Iterable, _dict: dict) -> bool:
    return all(k in _dict for k in required_keys)
