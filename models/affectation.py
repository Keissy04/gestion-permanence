from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Affectation(Base):
    __tablename__ = "affectations"

    id = Column(Integer, primary_key=True, index=True)
    id_employe = Column(Integer, ForeignKey("employes.id"), nullable=False)
    id_departement = Column(Integer, ForeignKey("departements.id"), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=True)

    employe = relationship("Employe")
    departement = relationship("Departement")
