from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.grade import Grade

router = APIRouter(tags=["Grade HTML"])
templates = Jinja2Templates(directory="app/templates")

# 📋 Liste des grades
@router.get("/grades", response_class=HTMLResponse)
def list_grades(request: Request, db: Session = Depends(get_db)):
    grades = db.query(Grade).all()
    return templates.TemplateResponse("views/grade/index.html", {"request": request, "grades": grades})


# ➕ Formulaire d'ajout
@router.get("/grades/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("views/grade/create.html", {"request": request, "error": ""})


# ✅ Traitement ajout
@router.post("/grades/create")
def create_grade(
    request: Request,
    titre: str = Form(...),
    abreviation: str = Form(...),
    db: Session = Depends(get_db)
):
    if not titre or not abreviation:
        return templates.TemplateResponse("views/grade/create.html", {
            "request": request,
            "error": "Tous les champs sont requis."
        })

    grade = Grade(titre=titre, abreviation=abreviation)
    db.add(grade)
    db.commit()
    return RedirectResponse(url="/grades", status_code=303)


# ✏️ Formulaire modification
@router.get("/grades/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    grade = db.query(Grade).filter(Grade.id == id).first()
    if not grade:
        return RedirectResponse(url="/grades", status_code=303)
    return templates.TemplateResponse("views/grade/edit.html", {
        "request": request,
        "grade": grade,
        "error": ""
    })


# 🔁 Traitement modification
@router.post("/grades/edit/{id}")
def update_grade(
    id: int,
    request: Request,
    titre: str = Form(...),
    abreviation: str = Form(...),
    db: Session = Depends(get_db)
):
    grade = db.query(Grade).filter(Grade.id == id).first()
    if grade:
        grade.titre = titre
        grade.abreviation = abreviation
        db.commit()
    return RedirectResponse(url="/grades", status_code=303)


# ❌ Suppression
@router.get("/grades/delete/{id}")
def delete_grade(id: int, db: Session = Depends(get_db)):
    grade = db.query(Grade).filter(Grade.id == id).first()
    if grade:
        db.delete(grade)
        db.commit()
    return RedirectResponse(url="/grades", status_code=303)
