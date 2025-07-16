from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Optional
from app.database import get_db
from app.models.employe_grade import EmployeGrade
from app.models.employe import Employe
from app.models.grade_par_poste import GradeParPoste

router = APIRouter(tags=["Affectation de grade"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/grade_employes", response_class=HTMLResponse)
def list_employe_grades(request: Request, db: Session = Depends(get_db), page: int = 1):
    per_page = 10
    total = db.query(EmployeGrade).count()
    pages = (total + per_page - 1) // per_page
    data = db.query(EmployeGrade).offset((page - 1) * per_page).limit(per_page).all()

    return templates.TemplateResponse("views/employe_grade/index.html", {
        "request": request,
        "relations": data,
        "page": page,
        "pages": pages
    })

@router.get("/employegrades/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db)):
    employes = db.query(Employe).all()
    gradeparpostes = db.query(GradeParPoste).all()
    return templates.TemplateResponse("views/employe_grade/create.html", {
        "request": request,
        "employes": employes,
        "gradeparpostes": gradeparpostes,
        "error": ""
    })


@router.post("/employegrades/create")
def create_relation(
    request: Request,
    id_employe: int = Form(...),
    id_grade_par_poste: int = Form(...),
    date_debut: date = Form(...),
    date_fin: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date() if date_fin else None
    except Exception:
        date_fin = None

    relation = EmployeGrade(
        id_employe=id_employe,
        id_grade_par_poste=id_grade_par_poste,
        date_debut=date_debut,
        date_fin=date_fin
    )
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return RedirectResponse(url="/grade_employes", status_code=303)


@router.get("/employegrades/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    relation = db.query(EmployeGrade).filter(EmployeGrade.id == id).first()
    employes = db.query(Employe).all()
    gradeparpostes = db.query(GradeParPoste).all()
    return templates.TemplateResponse("views/employe_grade/edit.html", {
        "request": request,
        "relation": relation,
        "employes": employes,
        "gradeparpostes": gradeparpostes,
        "error": ""
    })


@router.post("/employegrades/edit/{id}")
def update_relation(
    id: int,
    request: Request,
    id_employe: int = Form(...),
    id_grade_par_poste: int = Form(...),
    date_debut: date = Form(...),
    date_fin: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date() if date_fin else None
    except Exception:
        date_fin = None

    relation = db.query(EmployeGrade).filter(EmployeGrade.id == id).first()
    if relation:
        relation.id_employe = id_employe
        relation.id_grade_par_poste = id_grade_par_poste
        relation.date_debut = date_debut
        relation.date_fin = date_fin
        db.commit()
        db.refresh(relation)
    return RedirectResponse(url="/grade_employes", status_code=303)


@router.get("/employegrades/delete/{id}")
def delete_relation(id: int, db: Session = Depends(get_db)):
    relation = db.query(EmployeGrade).filter(EmployeGrade.id == id).first()
    if relation:
        db.delete(relation)
        db.commit()
    return RedirectResponse(url="/grade_employes", status_code=303)
