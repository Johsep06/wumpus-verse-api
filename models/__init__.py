from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from main import DB_CONFIG

db = create_engine(f'postgresql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["name"]}')

Base = declarative_base()