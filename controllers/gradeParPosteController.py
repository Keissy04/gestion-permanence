from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.grade_par_poste import GradeParPoste
from app.models.grade import Grade
from app.models.poste import Poste

router = APIRouter(tags=["Grade par Poste HTML"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/gradeparposte", response_class=HTMLResponse)
def list_gradeparposte(request: Request, db: Session = Depends(get_db)):
    relations = db.query(GradeParPoste).all()
    return templates.TemplateResponse("views/gradeparposte/index.html", {
        "request": request,
        "relations": relations
    })

@router.get("/gradeparposte/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db)):
    grades = db.query(Grade).all()
    postes = db.query(Poste).all()
    return templates.TemplateResponse("views/gradeparposte/create.html", {
        "request": request,
        "grades": grades,
        "postes": postes,
        "error": ""
    })

@router.post("/gradeparposte/create")
def create_relation(
    request: Request,
    id_grade: int = Form(...),
    id_poste: int = Form(...),
    db: Session = Depends(get_db)
):
    relation = GradeParPoste(id_grade=id_grade, id_poste=id_poste)
    db.add(relation)
    db.commit()
    return RedirectResponse(url="/gradeparposte", status_code=303)

@router.get("/gradeparposte/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    relation = db.query(GradeParPoste).filter(GradeParPoste.id == id).first()
    if not relation:
        return RedirectResponse(url="/gradeparposte", status_code=303)
    grades = db.query(Grade).all()
    postes = db.query(Poste).all()
    return templates.TemplateResponse("views/gradeparposte/edit.html", {
        "request": request,
        "relation": relation,
        "grades": grades,
        "postes": postes,
        "error": ""
    })

@router.post("/gradeparposte/edit/{id}")
def update_relation(
    id: int,
    request: Request,
    id_grade: int = Form(...),
    id_poste: int = Form(...),
    db: Session = Depends(get_db)
):
    relation = db.query(GradeParPoste).filter(GradeParPoste.id == id).first()
    if relation:
        relation.id_grade = id_grade
        relation.id_poste = id_poste
        db.commit()
    return RedirectResponse(url="/gradeparposte", status_code=303)

@router.get("/gradeparposte/delete/{id}")
def delete_relation(id: int, db: Session = Depends(get_db)):
    relation = db.query(GradeParPoste).filter(GradeParPoste.id == id).first()
    if relation:
        db.delete(relation)
        db.commit()
    return RedirectResponse(url="/gradeparposte", status_code=303)
