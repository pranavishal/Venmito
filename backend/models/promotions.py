from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Promotions(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_email = Column(String, ForeignKey('people.email'), nullable=False)
    phone = Column(String, nullable=True)
    promotion = Column(String, nullable=False)
    responded = Column(String, nullable=True)  # Will store 'yes' or 'no'