from sqlalchemy.orm import Session
from app.models.shop import Shop
from app.schemas.shop import ShopCreate

def create_shop(db: Session, shop: ShopCreate):
    db_shop = Shop(
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
    return db.query(Shop).first()
