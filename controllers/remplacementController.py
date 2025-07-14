from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.remplacement import Remplacement
from app.models.tour import Tour
from app.models.employe_grade import EmployeGrade
from app.models.permanence import Permanence

router = APIRouter(tags=["Remplacements HTML"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/remplacements", response_class=HTMLResponse)
def list_remplacements(request: Request, db: Session = Depends(get_db)):
    remplacements = db.query(Remplacement).all()
    return templates.TemplateResponse("views/remplacement/index.html", {
        "request": request,
        "remplacements": remplacements
    })

@router.get("/remplacements/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db)):
    employe_grades = db.query(EmployeGrade).all()
    tours = db.query(Tour).all()
    permanences = db.query(Permanence).all()
    return templates.TemplateResponse("views/remplacement/create.html", {
        "request": request,
        "employe_grades": employe_grades,
        "tours": tours,
        "permanences": permanences,
        "error": ""
    })

@router.post("/remplacements/create")
def create_remplacement(
    request: Request,
    id_employe_grade: int = Form(...),
    id_tour: int = Form(...),
    date_debut: date = Form(...),
    date_fin: date = Form(...),
    id_remplace: int = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    remplacement = Remplacement(
        id_employe_grade=id_employe_grade,
        id_tour=id_tour,
        date_debut=date_debut,
        date_fin=date_fin,
        id_remplace=id_remplace,
        description=description
    )
    db.add(remplacement)
    db.commit()
    return RedirectResponse(url="/remplacements", status_code=303)

@router.get("/remplacements/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    remplacement = db.query(Remplacement).filter(Remplacement.id == id).first()
    employe_grades = db.query(EmployeGrade).all()
    tours = db.query(Tour).all()
    permanences = db.query(Permanence).all()
    return templates.TemplateResponse("views/remplacement/edit.html", {
        "request": request,
        "remplacement": remplacement,
        "employe_grades": employe_grades,
        "tours": tours,
        "permanences": permanences,
        "error": ""
    })

@router.post("/remplacements/edit/{id}")
def update_remplacement(
    id: int,
    request: Request,
    id_employe_grade: int = Form(...),
    id_tour: int = Form(...),
    date_debut: date = Form(...),
    date_fin: date = Form(...),
    id_remplace: int = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    remplacement = db.query(Remplacement).filter(Remplacement.id == id).first()
    if remplacement:
        remplacement.id_employe_grade = id_employe_grade
        remplacement.id_tour = id_tour
        remplacement.date_debut = date_debut
        remplacement.date_fin = date_fin
        remplacement.id_remplace = id_remplace
        remplacement.description = description
        db.commit()
    return RedirectResponse(url="/remplacements", status_code=303)

@router.get("/remplacements/delete/{id}")
def delete_remplacement(id: int, db: Session = Depends(get_db)):
    remplacement = db.query(Remplacement).filter(Remplacement.id == id).first()
    if remplacement:
        db.delete(remplacement)
        db.commit()
    return RedirectResponse(url="/remplacements", status_code=303)
