from sqlalchemy import Column, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Remplacement(Base):
    __tablename__ = "remplacements"

    id = Column(Integer, primary_key=True, index=True)
    id_employe_grade = Column(Integer, ForeignKey("employe_grades.id"), nullable=False)
    id_tour = Column(Integer, ForeignKey("tours.id"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    id_remplace = Column(Integer, ForeignKey("permanences.id"), nullable=True)
    description = Column(Text, nullable=True)

    employe_grade = relationship("EmployeGrade")
    tour = relationship("Tour")
    remplace = relationship("Permanence")