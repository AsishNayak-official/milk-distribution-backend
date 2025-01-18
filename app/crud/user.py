from sqlalchemy.orm import Session
from .. import models, schemas

def create_user(db: Session, user: schemas.user.UserCreate, shop_id: str,id: str):
    db_user = models.user.User(
        id=id,
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
    return db.query(models.user.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: str, user_update: schemas.user.UserCreate):
    db_user = db.query(models.user.User).filter(models.user.User.id == user_id).first()

    if not db_user:
        return None

    # Update user attributes
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db.query(models.user.User).filter(models.user.User.id == user_id).delete()
    db.commit()
    
def get_user_by_id(db: Session, user_id: str):
    return db.query(models.user.User).filter(models.user.User.id == user_id).first()
