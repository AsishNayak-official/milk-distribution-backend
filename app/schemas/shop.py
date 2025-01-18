from pydantic import BaseModel
from typing import List
from .user import UserResponse

class ShopBase(BaseModel):
    society_name: str
    society_code: str
    unit: str
    month: str
    start_bill_date: str  
    end_bill_date: str    
    
class ShopCreate(ShopBase):
    pass
    
class ShopResponse(ShopBase):
    id: str
    # users: List[UserResponse]
    
class ShopUpdate(BaseModel):
    month: str
    start_bill_date: str  
    end_bill_date: str    


    class Config:
        from_attributes = True
