from sqlalchemy.orm import registry, relationship
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP


mapper_registry = registry()
Base = mapper_registry.generate_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    email = Column(String(64))

    def __repr__(self):
       return f"User(id={self.id!r}, name={self.name!r}"


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(TIMESTAMP)
    user = relationship("User")


class Chip(Base):
    __tablename__ = 'chip'
    id = Column(Integer, primary_key=True)
    iccid = Column(String(32))
    user = relationship("User")

# Base.metadata.create_all(engine)
