from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship  
from app.database import Base
import uuid

class Shop(Base):
    __tablename__ = "shops"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    society_name = Column(String)
    society_code = Column(String)
    unit = Column(String)
    month = Column(String)
    start_bill_date = Column(String)  
    end_bill_date = Column(String)

    # Define the relationship to the User model
    users = relationship("User", back_populates="shop")  # This sets up the relationship to the User model

