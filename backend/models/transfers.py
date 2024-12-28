from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Date, ForeignKey

Base = declarative_base()

class Transfers(Base):
    __tablename__ = 'transfers'

    transfer_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('people.id'))
    recipient_id = Column(Integer, ForeignKey('people.id'))
    amount = Column(Float)
    date = Column(Date)