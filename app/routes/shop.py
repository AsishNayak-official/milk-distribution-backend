from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.shop import ShopResponse,ShopCreate
from app.crud.shop import create_shop as crud_create_shop,get_shop_details as crud_get_shop_details
from app import database
router = APIRouter()

# Route to get shop details along with users
@router.get("/get-shop-details", response_model=ShopResponse)
def get_shop_details(db: Session = Depends(database.get_db)):
    shop_details = crud_get_shop_details(db=db)
    if shop_details is None:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop_details


@router.post("/create-shop/", response_model=ShopResponse)
def create_shop(shop: ShopCreate, db: Session = Depends(database.get_db)):
    return crud_create_shop(db=db, shop=shop)