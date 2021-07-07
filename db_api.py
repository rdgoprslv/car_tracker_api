from sqlalchemy import create_engine, text

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)


def get_maps_search_link(lat, lon):
    return f"https://www.google.com/maps/search/{lat:0.6f}%20{lon:0.6f}"


