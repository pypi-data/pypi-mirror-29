from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from settings import settings


engine = create_engine(settings['DATABASE'])

session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property()
Base.metadata.bind = engine
