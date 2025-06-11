from app.database.database import Base  # Explicitly import from database.py
from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, DateTime
from datetime import datetime  # Import only `datetime` class
from sqlalchemy import create_engine  # Import only `create_engine` function

class Destination(Base):
    __tablename__ = 'destinations'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    region = Column(String)
    season = Column(Enum('summer', 'winter', 'monsoon', name='seasons'))
    budget_range_low = Column(Float)
    budget_range_high = Column(Float)
    interests = Column(String)  # Store as comma-separated interests
    accommodation_type = Column(String)  # e.g., 'hotel', 'resort'
    travel_style = Column(String)  # e.g., 'luxury', 'budget'
    travel_duration = Column(Integer)  # in days
    travel_mode = Column(String)  # e.g., 'flight', 'train'
    special_requests = Column(String)  # e.g., 'vegan food'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    travel_experience = Column(String)  # e.g., 'first time', 'experienced'
    preferred_language = Column(String)  # e.g., 'English', 'Spanish'
    travel_group_type = Column(String)  # e.g., 'family', 'friends'
    travel_insurance = Column(Boolean, default=False)  # e.g., True or False
    travel_documents = Column(String)  # e.g., 'passport', 'visa'
    travel_activity_level = Column(String)  # e.g., 'low', 'medium', 'high'
    travel_dates = Column(String)  # Store as comma-separated dates
    travel_budget = Column(Float)  # Store as a single value
    travel_currency = Column(String)  # e.g., 'USD', 'EUR'
    travel_currency_rate = Column(Float)  # Store as a single value
    travel_currency_symbol = Column(String)  # e.g., '$', '€'
    travel_currency_conversion = Column(Float)  # Store as a single value
    travel_currency_conversion_rate = Column(Float)  # Store as a single value
    travel_currency_conversion_symbol = Column(String)  # e.g., '$', '€'
    travel_currency_conversion_date = Column(DateTime)  # Store as a single value
    travel_currency_conversion_rate_date = Column(DateTime)  # Store as a single value
    travel_currency_conversion_symbol_date = Column(DateTime)  # Store as a single value
    travel_currency_conversion_rate_symbol = Column(DateTime)  # Store as a single value
    travel_currency_conversion_rate_date_symbol = Column(DateTime)  # Store as a single value
    