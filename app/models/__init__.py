# app/models/__init__.py

from app.database import Base  # Import Base from database.py
from . import user  # Ensure 'user' is imported here
from . import shop # Import Shop model
    