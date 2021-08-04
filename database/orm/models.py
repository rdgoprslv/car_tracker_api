from json import dumps
from sqlalchemy.orm import registry, relationship
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey


mapper_registry = registry()
Base = mapper_registry.generate_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    email = Column(String(64), unique=True)
    chip = relationship("Chip", back_populates="user", uselist=False)

    def __repr__(self):
        return dumps(dict(id=self.id, name=self.name, email=self.email, chip=self.chip and self.chip.as_dict()))

    def as_dict(self):
        return dict(id=self.id, name=self.name, email=self.email, chip=self.chip)


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    def __repr__(self):
        return dumps(dict(id=self.id, lat=self.lat, lon=self.lon, timestamp=str(self.timestamp), user_id=self.user_id))

    def get_maps_search_link(self):
        return f"https://www.google.com/maps/search/{self.lat:0.6f}%20{self.lon:0.6f}"


class Chip(Base):
    __tablename__ = 'chip'
    id = Column(Integer, primary_key=True)
    iccid = Column(String(32), unique=True)

    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    user = relationship("User", back_populates='chip')

    def __repr__(self):
        return dumps(dict(id=self.id, iccid=self.iccid, user_id=self.user_id))

    def as_dict(self):
        return dict(id=self.id, iccid=self.iccid, user_id=self.user_id)

# historico de donos do chip?
