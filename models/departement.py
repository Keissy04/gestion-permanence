from sqlalchemy import Column, Integer, String
from app.database import Base

class Departement(Base):
    __tablename__ = "departements"

    id = Column(Integer, primary_key=True, index=True)
    dpt = Column(String, unique=True, nullable=False)
    abreviation = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mdp = Column(String, nullable=False) 
