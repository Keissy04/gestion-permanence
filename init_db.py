# init_db.py

from app.database import Base, engine
from app.models import employe_grade  # importe tous les modèles nécessaires

def init_db():
    Base.metadata.create_all(bind=engine)
