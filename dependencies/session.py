from sqlalchemy.orm import sessionmaker, Session
from models import engine

def get_session():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    finally:
        session.close()