from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Track(Base):
    __tablename__ = "tracks"
    id = Column(String, primary_key=True)
    name = Column(String)
    artist = Column(String)
    album = Column(String)
    played_at = Column(String, primary_key=True)


# Database connection
DATABASE_URL = "sqlite:///spotify_data.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)