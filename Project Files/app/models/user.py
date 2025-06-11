from pydantic import BaseModel
from typing import List

class UserDetails(BaseModel):
    budget: float
    interests: List[str]  # e.g., ['beach', 'mountains', 'historical sites']
    travel_season: str  # e.g., 'summer', 'winter', 'monsoon'
    preferred_accommodation: str  # e.g., 'hotel', 'resort', 'guesthouse'
    number_of_people: int
    travel_duration: int  # in days
    travel_style: str  # e.g., 'luxury', 'budget', 'adventure'
    travel_destination: str  # e.g., 'Europe', 'Asia', 'America'
    travel_dates: List[str]  # e.g., ['2023-06-01', '2023-06-15']
    travel_mode: str  # e.g., 'flight', 'train', 'car'
    special_requests: str  # e.g., 'vegan food', 'wheelchair accessible'
    travel_experience: str  # e.g., 'first time', 'experienced'
    preferred_language: str  # e.g., 'English', 'Spanish', 'French'
    travel_group_type: str  # e.g., 'family', 'friends', 'solo'
    travel_insurance: bool  # e.g., True or False
    travel_budget: float  # e.g., 1000.0
    travel_activity_level: str  # e.g., 'low', 'medium', 'high'


