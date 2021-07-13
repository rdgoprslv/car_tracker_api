from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)
Session = sessionmaker(engine, autocommit=False)
