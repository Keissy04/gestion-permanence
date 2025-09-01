from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Remplacant(Base):
    __tablename__ = "remplacants"

    id = Column(Integer, primary_key=True, index=True)
    id_employe_grade = Column(Integer, ForeignKey("employe_grades.id"), nullable=False)
    id_tour = Column(Integer, ForeignKey("tours.id"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)

    employe_grade = relationship("EmployeGrade")
    tour = relationship("Tour")