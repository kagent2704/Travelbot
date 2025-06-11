from app.models.destination import Destination
from sqlalchemy.orm import Session
from app.models.user import UserDetails

def recommend_destinations(user: UserDetails, db: Session):
    # Query the database for destinations that match user preferences
    recommendations = db.query(Destination).filter(
        Destination.budget_range_low <= user.budget,
        Destination.budget_range_high >= user.budget,
        Destination.season == user.travel_season,
        Destination.accommodation_type == user.preferred_accommodation
    ).all()
    
    # Further filter by interests
    filtered_recommendations = [
        dest for dest in recommendations if any(interest in dest.interests.split(",") for interest in user.interests)
    ]
    
    return filtered_recommendations
