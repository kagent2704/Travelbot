from app.database.database import Base, engine  # Ensure the correct import
from app.models.destination import Destination
from app.models.user import UserDetails

# Create tables
Base.metadata.create_all(bind=engine)
