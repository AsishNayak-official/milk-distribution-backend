from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    shop_id = Column(String, ForeignKey("shops.id"))
    name = Column(String)
    membership_no = Column(Integer)
    milk_supplied = Column(Float)
    total_qty_milk_supplied = Column(Float)
    fat_percentage = Column(Float)
    snf_percentage = Column(Float)
    adhaar = Column(String)
    bank_name = Column(String)
    branch_name = Column(String)
    account_number = Column(String)
    ifsc_code = Column(String)

    shop = relationship("Shop", back_populates="users")
