from sqlalchemy.orm import Session
from app import models,schemas

def create_shop(db: Session, shop: schemas.shop.ShopCreate):
    db_shop = models.shop.Shop(
        society_name=shop.society_name,
        society_code=shop.society_code,
        unit=shop.unit,
        month=shop.month,
        start_bill_date=shop.start_bill_date,
        end_bill_date=shop.end_bill_date,
    )
    db.add(db_shop)
    try:
        db.commit()  # Commit the transaction
        db.refresh(db_shop)  # Refresh the instance to get the ID
        return db_shop
    except Exception as e:
        db.rollback()  # Rollback the transaction on error
        print(f"Error creating shop: {e}")  # Log the error for debugging
        raise e


def get_shop_details(db: Session):
    return db.query(models.shop.Shop).first()

def update_shop_dates(db: Session, shop_id: str, shop_update: schemas.shop.ShopUpdate):
    db_shop = db.query(models.shop.Shop).filter(models.shop.Shop.id == shop_id).first()
    if db_shop:
        db_shop.start_bill_date = shop_update.start_bill_date
        db_shop.end_bill_date = shop_update.end_bill_date
        db_shop.month = shop_update.month
        db.commit()
        db.refresh(db_shop)
        return db_shop
    return None

def get_shop_if_exists(db: Session, society_code: str):
    return db.query(models.shop.Shop).filter(models.shop.Shop.society_code == society_code).first()

def delete_shop(db: Session, shop_id: str):
    db.query(models.shop.Shop).filter(models.shop.Shop.id == shop_id).delete()
    db.commit()
    
def get_shop_by_id(db: Session, shop_id: str):
    return db.query(models.shop.Shop).filter(models.shop.Shop.id == shop_id).first()