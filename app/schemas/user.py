from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    name: str
    membership_no: int
    milk_supplied: float | None
    total_qty_milk_supplied: float | None
    fat_percentage: float | None
    snf_percentage: float | None
    adhaar: str
    bank_name: str
    branch_name: str
    account_number: str
    ifsc_code: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: str

class UserListResponse(BaseModel):
    shop_id: str | None = None
    data: List[UserResponse]
    
    class Config:
        from_attributes = True
