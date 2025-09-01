from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.remplacant import Remplacant
from app.models.employe_grade import EmployeGrade
from app.models.tour import Tour 

router = APIRouter(tags=["Remplaçants HTML"])
templates = Jinja2Templates(directory="app/templates")



@router.get("/remplacants", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    remplacants = db.query(Remplacant).all()
    return templates.TemplateResponse("views/remplacant/index.html", {
        "request": request,
        "remplacants": remplacants
    })


@router.get("/remplacants/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db)):
    employe_grades = db.query(EmployeGrade).all()
    tours = db.query(Tour).all()
    return templates.TemplateResponse("views/remplacant/create.html", {
        "request": request,
        "employe_grades": employe_grades,
        "tours": tours,
        "error": ""
    })
    


@router.post("/remplacants/create")
def create(
    id_employe_grade: int = Form(...),
    date_debut: date = Form(...),
    date_fin: date = Form(None),
    id_tour: int = Form(...),
    db: Session = Depends(get_db)
):
    remplacant = Remplacant(
        id_tour=id_tour,
        id_employe_grade=id_employe_grade,
        date_debut=date_debut,
        date_fin=date_fin
    )
    db.add(remplacant)
    db.commit()
    return RedirectResponse(url="/remplacants", status_code=303)


@router.get("/remplacants/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    remplacant = db.query(Remplacant).filter_by(id=id).first()
    employe_grades = db.query(EmployeGrade).all()
    tours = db.query(Tour).all()
    return templates.TemplateResponse("views/remplacant/edit.html", {
        "request": request,
        "remplacant": remplacant,
        "tours": tours,
        "employe_grades": employe_grades,
        "error": ""
    })



@router.post("/remplacants/edit/{id}")
def edit(
    id: int,
    id_employe_grade: int = Form(...),
    date_debut: date = Form(...),
    date_fin: date = Form(None),
    id_tour: int = Form(...),
    db: Session = Depends(get_db)
):
    remplacant = db.query(Remplacant).filter_by(id=id).first()
    if remplacant:
        remplacant.id_employe_grade = id_employe_grade
        remplacant.date_debut = date_debut
        remplacant.date_fin = date_fin
        remplacant.id_tour = id_tour
        db.commit()
    return RedirectResponse(url="/remplacants", status_code=303)



@router.get("/remplacants/delete/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    remplacant = db.query(Remplacant).filter_by(id=id).first()
    if remplacant:
        db.delete(remplacant)
        db.commit()
    return RedirectResponse(url="/remplacants", status_code=303)
