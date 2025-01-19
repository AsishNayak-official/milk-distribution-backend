from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.orm import relationship  
from app.database import Base
import uuid
from datetime import datetime


class Shop(Base):
    __tablename__ = "shops"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    society_name = Column(String)
    society_code = Column(String)
    unit = Column(String)
    month = Column(String)
    start_bill_date = Column(String)  
    end_bill_date = Column(String)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    # Define the relationship to the User model
    users = relationship("User", back_populates="shop")  # This sets up the relationship to the User model

