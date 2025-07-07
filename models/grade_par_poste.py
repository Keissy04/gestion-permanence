from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GradeParPoste(Base):
    __tablename__ = "grade_par_poste"

    id = Column(Integer, primary_key=True, index=True)
    id_grade = Column(Integer, ForeignKey("grades.id"), nullable=False)
    id_poste = Column(Integer, ForeignKey("postes.id"), nullable=False)

    grade = relationship("Grade")
    poste = relationship("Poste")
