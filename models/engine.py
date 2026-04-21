from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from main import DB_CONFIG

DATABASE_URL = (
    f'postgresql+psycopg2://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}'
    f'@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["name"]}'
    '?sslmode=require'
)

engine = create_engine(DATABASE_URL)

Base = automap_base()
Base.prepare(autoload_with=engine)
