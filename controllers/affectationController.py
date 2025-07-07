from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.database import get_db
from app.models.affectation import Affectation
from app.models.employe_grade import EmployeGrade
from app.models.departement import Departement

router = APIRouter(tags=["Affectations HTML"])
templates = Jinja2Templates(directory="app/templates")

# Liste
@router.get("/affectations", response_class=HTMLResponse)
def list_affectations(request: Request, db: Session = Depends(get_db)):
    affectations = db.query(Affectation).all()
    return templates.TemplateResponse("views/affectation/index.html", {
        "request": request,
        "affectations": affectations
    })

# Formulaire création
@router.get("/affectations/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db)):
    employe_grades = db.query(EmployeGrade).all()
    departements = db.query(Departement).all()
    return templates.TemplateResponse("views/affectation/create.html", {
        "request": request,
        "employe_grades": employe_grades,
        "departements": departements,
        "error": ""
    })

# Traitement création
@router.post("/affectations/create")
def create_affectation(
    request: Request,
    id_employe_grade: int = Form(...),
    id_departement: int = Form(...),
    date_debut: date = Form(...),
    date_fin: Optional[str] = Form(None),  # ← accepte chaîne vide
    db: Session = Depends(get_db)
):
    affectation = Affectation(
        id_employe_grade=id_employe_grade,
        id_departement=id_departement,
        date_debut=date_debut,
        date_fin=date.fromisoformat(date_fin) if date_fin else None
    )
    db.add(affectation)
    db.commit()
    return RedirectResponse(url="/affectations", status_code=303)

# Formulaire modification
@router.get("/affectations/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    affectation = db.query(Affectation).filter(Affectation.id == id).first()
    employe_grades = db.query(EmployeGrade).all()
    departements = db.query(Departement).all()
    return templates.TemplateResponse("views/affectation/edit.html", {
        "request": request,
        "affectation": affectation,
        "employe_grades": employe_grades,
        "departements": departements,
        "error": ""
    })

# Traitement modification
@router.post("/affectations/edit/{id}")
def update_affectation(
    id: int,
    request: Request,
    id_employe_grade: int = Form(...),
    id_departement: int = Form(...),
    date_debut: date = Form(...),
    date_fin: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    affectation = db.query(Affectation).filter(Affectation.id == id).first()
    if affectation:
        affectation.id_employe_grade = id_employe_grade
        affectation.id_departement = id_departement
        affectation.date_debut = date_debut
        affectation.date_fin = date.fromisoformat(date_fin) if date_fin else None
        db.commit()
    return RedirectResponse(url="/affectations", status_code=303)

# Suppression
@router.get("/affectations/delete/{id}")
def delete_affectation(id: int, db: Session = Depends(get_db)):
    affectation = db.query(Affectation).filter(Affectation.id == id).first()
    if affectation:
        db.delete(affectation)
        db.commit()
    return RedirectResponse(url="/affectations", status_code=303)
