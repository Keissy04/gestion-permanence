from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Permanence(Base):
    __tablename__ = "permanences"

    id = Column(Integer, primary_key=True, index=True)
    id_employe_grade = Column(Integer, ForeignKey("employe_grades.id"), nullable=False)
    date_permanence = Column(Date, nullable=False)
    is_remplace = Column(Boolean, default=False)

    employe_grade = relationship("EmployeGrade")
