from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Affectation(Base):
    __tablename__ = "affectations"

    id = Column(Integer, primary_key=True, index=True)
    id_employe_grade = Column(Integer, ForeignKey("employe_grades.id"), nullable=False)
    id_departement = Column(Integer, ForeignKey("departements.id"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=True)

    employe_grade = relationship("EmployeGrade", back_populates="affectations")
    departement = relationship("Departement")
    
