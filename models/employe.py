from sqlalchemy import Column, Integer, String
from app.database import Base

class Employe(Base):
    __tablename__ = "employes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
