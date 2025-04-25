from sqlalchemy.orm import Session
from .. import models, schemas

def create_user(db: Session, user_data: dict, shop_id: str,id: str):
    db_user = models.user.User(
        id=id,
        shop_id=shop_id,
        name=user_data.get("name"),
        membership_no=user_data.get("membership_no"),
        milk_supplied=user_data.get("milk_supplied"),
        total_qty_milk_supplied=user_data.get("total_qty_milk_supplied"),
        fat_percentage=user_data.get("fat_percentage"),
        snf_percentage=user_data.get("snf_percentage"),
        adhaar=user_data.get("adhaar"),
        bank_name=user_data.get("bank_name"),
        branch_name=user_data.get("branch_name"),
        account_number=user_data.get("account_number"),
        ifsc_code=user_data.get("ifsc_code"),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user.User).order_by(models.user.User.created_at).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: str, user_data: dict):
    db_user = db.query(models.user.User).filter(models.user.User.id == user_id).first()

    if not db_user:
        return None

    # Update user attributes
    for key, value in user_data.items():
        if key in models.user.User.__table__.columns:
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db.query(models.user.User).filter(models.user.User.id == user_id).delete()
    db.commit()
    
def get_user_by_id(db: Session, user_id: str):
    return db.query(models.user.User).filter(models.user.User.id == user_id).first()
