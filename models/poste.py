from sqlalchemy import Column, Integer, String
from app.database import Base

class Poste(Base):
    __tablename__ = "postes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)
