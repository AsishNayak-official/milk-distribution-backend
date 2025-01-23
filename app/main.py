from fastapi import FastAPI
from app.routes import user, shop
from app.database import engine
from app.models import Base 
from fastapi.middleware.cors import CORSMiddleware

# Create tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins (any domain)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)



# Include routers for user and shop endpoints
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(shop.router, prefix="/shop", tags=["shops"])
