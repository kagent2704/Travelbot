from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import UserDetails
from app.services.recommendations import recommend_destinations
from app.database import get_db


router = APIRouter()

@router.post("/recommendations/")
async def get_recommendations(user: UserDetails, db: Session = Depends(get_db)):
    recommendations = recommend_destinations(user, db)
    
    return {"recommended_destinations": recommendations}
