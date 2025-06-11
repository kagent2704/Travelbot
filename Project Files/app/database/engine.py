from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./test.db"  # Change to your database URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
