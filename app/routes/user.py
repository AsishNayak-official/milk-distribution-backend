from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app import database
from app import crud
import uuid
from fastapi import HTTPException


router = APIRouter()

# Route to add a user
@router.patch("/upsert-user/", response_model=schemas.user.UserResponse)
def upsert_user(
    user_data: dict,
    shop_id: str,
    user_id: str | None = None,  # Optional user_id
    db: Session = Depends(database.get_db)
):
    if user_id:
        # Update user info if user_id is provided
        updated_user = crud.user.update_user(db=db, user_id=user_id, user_data=user_data)
        if not updated_user:
            raise HTTPException(status_code=400, detail="User not found")
        return updated_user
    else:
        if "membership_no" not in user_data or "name" not in user_data:
            raise HTTPException(
                status_code=400,
                detail="Both 'membership_no' and 'name' are required to create a user"
            )
        user_uuid = uuid.uuid4()  # Generate a new UUID for the user
        new_user = crud.user.create_user(db=db, user_data=user_data, shop_id=shop_id, id=str(user_uuid))
        return new_user

# Route to get all users
@router.get("/get-all-users/", response_model= schemas.user.UserListResponse)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.user.get_users(db=db, skip=skip, limit=limit)
    if not users:
        return {"shop_id": None, "data": []}
    
    shop_id = users[0].shop_id
    return {"shop_id": shop_id,"data": users}


@router.delete("/delete-user/{user_id}", response_model=schemas.user.UserResponse)
def delete_user(user_id: str, db: Session = Depends(database.get_db)):
    # Check if user exists before deleting
    user = crud.user.get_user_by_id(db, user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Proceed to delete the user
    crud.user.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}