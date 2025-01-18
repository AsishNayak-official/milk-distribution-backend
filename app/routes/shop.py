from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.shop import ShopResponse,ShopCreate,ShopUpdate
from app.crud.shop import create_shop as crud_create_shop,get_shop_details as crud_get_shop_details,update_shop_dates as crud_update_shop_dates
from app import database
router = APIRouter()

# Route to get shop details along with users
@router.get("/get-shop-details", response_model=ShopResponse)
def get_shop_details(db: Session = Depends(database.get_db)):
    shop_details = crud_get_shop_details(db=db)
    if shop_details is None:
        raise HTTPException(status_code=400, detail="Shop not found")
    return shop_details


@router.post("/create-shop/", response_model=ShopResponse)
def create_shop(shop: ShopCreate, db: Session = Depends(database.get_db)):
    return crud_create_shop(db=db, shop=shop)

@router.patch("/update-shop-dates/{shop_id}", response_model=ShopResponse)
def update_shop_dates(shop_id: str, shop_update: ShopUpdate, db: Session = Depends(database.get_db)):
    updated_shop = crud_update_shop_dates(db=db, shop_id=shop_id, shop_update=shop_update)
    if not updated_shop:
        raise HTTPException(status_code=400, detail="Shop not found")
    return updated_shop