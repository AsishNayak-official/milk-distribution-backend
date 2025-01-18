from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas,crud,models
from app import database
from fastapi import HTTPException

router = APIRouter()

# Route to get shop details along with users
@router.get("/get-shop-details", response_model=schemas.shop.ShopResponse)
def get_shop_details(db: Session = Depends(database.get_db)):
    shop_details = crud.shop.get_shop_details(db=db)
    if shop_details is None:
        raise HTTPException(status_code=400, detail="Shop not found")
    return shop_details


@router.post("/create-shop/", response_model=schemas.shop.ShopResponse)
def create_shop(shop: models.shop.ShopCreate, db: Session = Depends(database.get_db)):
    return crud.shop.create_shop(db=db, shop=shop)

@router.patch("/update-shop-dates/{shop_id}", response_model=schemas.shop.ShopResponse)
def update_shop_dates(shop_id: str, shop_update: models.shop.ShopUpdate, db: Session = Depends(database.get_db)):
    updated_shop = crud.shop.update_shop_dates(db=db, shop_id=shop_id, shop_update=shop_update)
    if not updated_shop:
        raise HTTPException(status_code=400, detail="Shop not found")
    return updated_shop

@router.delete("/delete-shop/{shop_id}", response_model=schemas.shop.ShopResponse)
def delete_user(shop_id: str, db: Session = Depends(database.get_db)):
    # Check if user exists before deleting
    shop = crud.shop.get_shop_by_id(db, shop_id=shop_id)
    
    if not shop:
        raise HTTPException(status_code=400, detail="Shop not found")
    
    # Proceed to delete the user
    crud.shop.delete_shop(db=db, shop_id=shop_id)
    return {"message": "Shop deleted successfully"}