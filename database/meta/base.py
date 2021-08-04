import os

DB_TECH = os.environ.get('DB_TECH',         "sqlite")
DB_ADAPTER = os.environ.get('DB_ADAPTER',   "pysqlite")
DB_USER = os.environ.get('DB_USER',         "postgres")
DB_PASS = os.environ.get('DB_PASS',         "postgres")
DB_SERVICE = os.environ.get('DB_SERVICE',   "localhost")
DB_PORT = os.environ.get('DB_PORT',         "5432")
DB_NAME = os.environ.get('DB_NAME',         "car_tracker")

if DB_TECH == "sqlite":
    database_url = 'sqlite+pysqlite:///sqlite.db'
else:
    database_url = '{DB_TECH}+{DB_ADAPTER}://{DB_USER}:{DB_PASS}@{DB_SERVICE}:{DB_PORT}/{DB_NAME}'
