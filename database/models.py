from sqlalchemy.orm import registry, relationship
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey


mapper_registry = registry()
Base = mapper_registry.generate_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    email = Column(String(64))
    locations = relationship("Locations")
    chip = relationship("Chip", back_populates="user", uselist=False)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(TIMESTAMP)
    user = Column(Integer, ForeignKey('user.id'))

    def get_maps_search_link():
        return f"https://www.google.com/maps/search/{self.lat:0.6f}%20{self.lon:0.6f}"


class Chip(Base):
    __tablename__ = 'chip'
    id = Column(Integer, primary_key=True)
    iccid = Column(String(32))

    chip = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates='chip')


# historico de donos do chip?
