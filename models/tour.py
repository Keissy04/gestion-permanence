from sqlalchemy import Column, Integer, String
from app.database import Base

class Tour(Base):
    __tablename__ = "tours"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), unique=True, nullable=False)
