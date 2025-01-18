from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserCreate
from app import database
router = APIRouter()

# Route to add a user
@router.post("/create-new-user/", response_model=UserResponse)
def add_user(user: UserCreate, shop_id: int, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user, shop_id=shop_id)

@router.patch("/update-user-info/{user_id}", response_model=UserResponse)
def update_user_info(user_id: int, user_update: UserCreate, db: Session = Depends(database.get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)

    if not updated_user:
        raise HTTPException(status_code=400, detail="User not found")

    return updated_user

# Route to get all users
@router.get("/get-all-users/", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


