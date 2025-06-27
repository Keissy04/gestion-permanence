from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.departement import Departement

router = APIRouter(tags=["Département HTML"])
templates = Jinja2Templates(directory="app/templates")

# 📋 Liste des départements
@router.get("/departements", response_class=HTMLResponse)
def list_departements(request: Request, db: Session = Depends(get_db)):
    departements = db.query(Departement).all()
    return templates.TemplateResponse("views/departement/index.html", {
        "request": request,
        "departements": departements
    })


# ➕ Formulaire d'ajout
@router.get("/departements/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("views/departement/create.html", {
        "request": request,
        "error": ""
    })


# ✅ Traitement de l'ajout
@router.post("/departements/create")
def create_depart(
    request: Request,
    dpt: str = Form(...),
    abreviation: str = Form(...),
    db: Session = Depends(get_db)
):
    if not dpt or not abreviation:
        return templates.TemplateResponse("views/departement/create.html", {
            "request": request,
            "error": "Tous les champs sont requis."
        })

    departement = Departement(dpt=dpt, abreviation=abreviation)
    db.add(departement)
    db.commit()
    return RedirectResponse(url="/departements", status_code=303)


# 📝 Formulaire de modification
@router.get("/departements/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    departement = db.query(Departement).filter(Departement.id == id).first()
    if not departement:
        return RedirectResponse(url="/departements", status_code=303)
    return templates.TemplateResponse("views/departement/edit.html", {
        "request": request,
        "departement": departement,
        "error": ""
    })


# 🔁 Traitement de modification
@router.post("/departements/edit/{id}")
def update_depart(
    id: int,
    request: Request,
    dpt: str = Form(...),
    abreviation: str = Form(...),
    db: Session = Depends(get_db)
):
    if not dpt or not abreviation:
        departement = db.query(Departement).filter(Departement.id == id).first()
        return templates.TemplateResponse("views/departement/edit.html", {
            "request": request,
            "departement": departement,
            "error": "Tous les champs sont requis."
        })

    departement = db.query(Departement).filter(Departement.id == id).first()
    if departement:
        departement.dpt = dpt
        departement.abreviation = abreviation
        db.commit()
    return RedirectResponse(url="/departements", status_code=303)


# ❌ Suppression d'un département
@router.get("/departements/delete/{id}")
def delete_depart(id: int, db: Session = Depends(get_db)):
    departement = db.query(Departement).filter(Departement.id == id).first()
    if departement:
        db.delete(departement)
        db.commit()
    return RedirectResponse(url="/departements", status_code=303)
