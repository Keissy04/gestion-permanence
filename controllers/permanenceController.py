from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.permanence import Permanence
from app.models.employe_grade import EmployeGrade

router = APIRouter(tags=["Permanences HTML"])
templates = Jinja2Templates(directory="app/templates")

# --- Liste des permanences ---
@router.get("/permanences", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    permanences = db.query(Permanence).all()
    return templates.TemplateResponse("views/permanence/index.html", {
        "request": request,
        "permanences": permanences
    })

# --- Formulaire de création ---
@router.get("/permanences/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db)):
    employe_grades = db.query(EmployeGrade).all()
    return templates.TemplateResponse("views/permanence/create.html", {
        "request": request,
        "employe_grades": employe_grades,
        "error": ""
    })

# --- Traitement création ---
@router.post("/permanences/create")
def create(
    id_employe_grade: int = Form(...),
    date_permanence: date = Form(...),
    db: Session = Depends(get_db)
):
    permanence = Permanence(
        id_employe_grade=id_employe_grade,
        date_permanence=date_permanence
    )
    db.add(permanence)
    db.commit()
    return RedirectResponse(url="/permanences", status_code=303)

# --- Formulaire de modification ---
@router.get("/permanences/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    permanence = db.query(Permanence).filter_by(id=id).first()
    employe_grades = db.query(EmployeGrade).all()
    return templates.TemplateResponse("views/permanence/edit.html", {
        "request": request,
        "permanence": permanence,
        "employe_grades": employe_grades,
        "error": ""
    })

# --- Traitement modification ---
@router.post("/permanences/edit/{id}")
def edit(
    id: int,
    id_employe_grade: int = Form(...),
    date_permanence: date = Form(...),
    db: Session = Depends(get_db)
):
    permanence = db.query(Permanence).filter_by(id=id).first()
    permanence.id_employe_grade = id_employe_grade
    permanence.date_permanence = date_permanence
    db.commit()
    return RedirectResponse(url="/permanences", status_code=303)

# --- Suppression ---
@router.get("/permanences/delete/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    permanence = db.query(Permanence).filter_by(id=id).first()
    if permanence:
        db.delete(permanence)
        db.commit()
    return RedirectResponse(url="/permanences", status_code=303)
