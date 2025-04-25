import os
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app import schemas,crud,models
from app import database
from fastapi import HTTPException

from app.utils.pdf_generator import create_docx

router = APIRouter()

# Route to get shop details along with users
@router.get("/get-shop-details", response_model=schemas.shop.ShopResponse)
def get_shop_details(db: Session = Depends(database.get_db)):
    shop_details = crud.shop.get_shop_details(db=db)
    if shop_details is None:
        raise HTTPException(status_code=400, detail="No shop details found.")
    return shop_details


@router.post("/create-shop/", response_model=schemas.shop.ShopResponse)
def create_shop(shop: schemas.shop.ShopCreate, db: Session = Depends(database.get_db)):
    if not shop.society_name or not shop.society_code:
        raise HTTPException(status_code=400, detail="Society name and code are required.")
    return crud.shop.create_shop(db=db, shop=shop)

@router.patch("/update-shop-dates/{shop_id}", response_model=schemas.shop.ShopResponse)
def update_shop_dates(shop_id: str, shop_update: schemas.shop.ShopUpdate, db: Session = Depends(database.get_db)):
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

@router.get("/download/{shop_id}")
def download_doc(shop_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    # Fetch shop details
    shop = crud.shop.get_shop_by_id(db, shop_id=shop_id)
    if not shop:
        raise HTTPException(status_code=400, detail="Shop not found")

    # Fetch users for the shop
    users = crud.user.get_users(db=db, skip=skip, limit=limit)

    # Prepare context for the template
    context = {
        "society_name": shop.society_name,
        "society_code": shop.society_code,
        "unit": shop.unit,
        "month": shop.month,  
        "start_date": shop.start_bill_date,
        "end_date": shop.end_bill_date,
        "members": [
            {
                "name": user.name or "",
                "membership_no": user.membership_no or "",
                "milk_supplied": user.milk_supplied or "",
                "total_qty_milk_supplied": user.total_qty_milk_supplied or "",
                "fat_percentage": user.fat_percentage or "",
                "snf_percentage": user.snf_percentage or "",
                "aadhaar": user.adhaar or "",
                "bank_name": user.bank_name or "",
                "branch_name": user.branch_name or "",
                "account_number": user.account_number or "",
                "ifsc_code": user.ifsc_code or "",
            }
            for user in users
        ],
    }

    # Generate PDF
    output_file = f"{shop.society_name}_{shop.start_bill_date}_{shop.end_bill_date}_report.docx"
    create_docx(context, output_file)

    # Serve PDF as a downloadable response
    with open(output_file, "rb") as file:
        file_bytes = file.read()

    # Cleanup temporary file
    os.remove(output_file)

    return Response(
        file_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename={shop.society_name}_{shop.start_bill_date}_{shop.end_bill_date}_report.docx"
        }, 
    )