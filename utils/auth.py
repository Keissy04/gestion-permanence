from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.departement import Departement

def get_current_departement(
    request: Request,
    db: Session = Depends(get_db)
) -> Departement:
    dpt_id = request.session.get("departement_id")
    if not dpt_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non authentifié")
    dpt = db.query(Departement).get(dpt_id)
    if not dpt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session invalide")
    return dpt
