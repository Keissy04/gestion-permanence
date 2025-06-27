from sqlalchemy import Column, Integer, String
from app.database import Base

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)
    abreviation = Column(String, nullable=False)
