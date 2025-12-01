from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from .db import Base

class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    old_price = Column(Float)
    discount = Column(Float)
    store = Column(String)
    url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
