from fastapi import FastAPI
from .routes import user, shop
from .database import engine
from app.models import Base 

# Create tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers for user and shop endpoints
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(shop.router, prefix="/shop", tags=["shops"])
