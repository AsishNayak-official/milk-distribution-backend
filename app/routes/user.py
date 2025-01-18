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
    user: schemas.user.UserCreate,
    shop_id: str,
    user_id: str | None = None,  # Optional user_id
    db: Session = Depends(database.get_db)
):
    if user_id:
        # Update user info if user_id is provided
        updated_user = crud.user.update_user(db=db, user_id=user_id, user_update=user)
        if not updated_user:
            raise HTTPException(status_code=400, detail="User not found")
        return updated_user
    else:
        user_uuid = uuid.uuid4()  # Generate a new UUID for the user
        new_user = crud.user.create_user(db=db, user=user, shop_id=shop_id, id=str(user_uuid))
        return new_user

# Route to get all users
@router.get("/get-all-users/", response_model= schemas.user.UserListResponse)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.user.get_users(db=db, skip=skip, limit=limit)
    

    return {"data": users}


