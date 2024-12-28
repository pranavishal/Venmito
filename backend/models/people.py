from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()

class People(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    firstName = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    Android = Column(Boolean, nullable=True)
    iPhone = Column(Boolean, nullable=True)
    Desktop = Column(Boolean, nullable=True)
