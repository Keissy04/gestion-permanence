from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class EmployeGrade(Base):
    __tablename__ = "employe_grades"

    id = Column(Integer, primary_key=True, index=True)
    id_employe = Column(Integer, ForeignKey("employes.id"), nullable=False)
    id_grade_par_poste = Column(Integer, ForeignKey("grade_par_poste.id"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=True)

    employe = relationship("Employe")
    grade_par_poste = relationship("GradeParPoste")
