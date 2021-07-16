from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import database_url
from .models import mapper_registry
from .db import Db


engine = create_engine(database_url, echo=False, future=True)
Session = sessionmaker(engine, autocommit=False)


def create_db():
    mapper_registry.metadata.create_all(engine)


def delete_db():
    mapper_registry.metadata.drop_all(bind=engine)


def get_db_obj():
    return Db(session_maker=Session)
