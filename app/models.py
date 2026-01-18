from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    value = Column(Float)
    purchase_date = Column(Date)
    status = Column(String)

