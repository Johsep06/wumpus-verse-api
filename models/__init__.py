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

User = Base.classes.usuario
EnvironmentDb = Base.classes.ambiente
RoomDb = Base.classes.sala
RoomObject = Base.classes.sala_objeto
AgentDB = Base.classes.primeiro_agente
ThirdAgentDB = Base.classes.terceiro_agente

__all__ = [
    'engine',
    'Base',
    'User',
    'EnvironmentDb',
    'RoomDb',
    'RoomObject',
    'AgentDB',
    'ThirdAgentDB',
]
