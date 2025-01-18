from sqlalchemy.orm import Session
from .. import models, schemas

def create_user(db: Session, user: schemas.UserCreate, shop_id: int):
    db_user = models.User(
        shop_id=shop_id,
        name=user.name,
        membership_no=user.membership_no,
        milk_supplied=user.milk_supplied,
        total_qty_milk_supplied=user.total_qty_milk_supplied,
        fat_percentage=user.fat_percentage,
        snf_percentage=user.snf_percentage,
        adhaar=user.adhaar,
        bank_name=user.bank_name,
        branch_name=user.branch_name,
        account_number=user.account_number,
        ifsc_code=user.ifsc_code
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: schemas.UserCreate):
    # Fetch the user by id
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        return None

    # Update user attributes
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    # Commit the changes
    db.commit()
    db.refresh(db_user)
    return db_user