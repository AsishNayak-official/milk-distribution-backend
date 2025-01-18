from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    name: str
    membership_no: str
    milk_supplied: float
    total_qty_milk_supplied: float
    fat_percentage: float
    snf_percentage: float
    adhaar: str
    bank_name: str
    branch_name: str
    account_number: str
    ifsc_code: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

class UserListResponse(BaseModel):
    data: List[UserResponse]
    
    class Config:
        orm_mode = True
