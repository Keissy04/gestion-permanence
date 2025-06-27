from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.poste import Poste

router = APIRouter(tags=["Postes HTML"])
templates = Jinja2Templates(directory="app/templates")

# Liste
@router.get("/postes", response_class=HTMLResponse)
def list_postes(request: Request, db: Session = Depends(get_db)):
    postes = db.query(Poste).all()
    return templates.TemplateResponse("views/poste/index.html", {"request": request, "postes": postes})

# Formulaire de création
@router.get("/postes/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("views/poste/create.html", {"request": request, "error": ""})

# Traitement de création
@router.post("/postes/create")
def create_poste(
    request: Request,
    nom: str = Form(...),
    db: Session = Depends(get_db)
):
    if not nom:
        return templates.TemplateResponse("views/poste/create.html", {
            "request": request,
            "error": "Le nom du poste est requis."
        })

    poste = Poste(nom=nom)
    db.add(poste)
    db.commit()
    return RedirectResponse(url="/postes", status_code=303)

# Formulaire d'édition
@router.get("/postes/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    poste = db.query(Poste).filter(Poste.id == id).first()
    if not poste:
        return RedirectResponse(url="/postes", status_code=303)
    return templates.TemplateResponse("views/poste/edit.html", {
        "request": request,
        "poste": poste,
        "error": ""
    })

# Traitement d'édition
@router.post("/postes/edit/{id}")
def update_poste(
    id: int,
    request: Request,
    nom: str = Form(...),
    db: Session = Depends(get_db)
):
    poste = db.query(Poste).filter(Poste.id == id).first()
    if poste:
        poste.nom = nom
        db.commit()
    return RedirectResponse(url="/postes", status_code=303)

# Suppression
@router.get("/postes/delete/{id}")
def delete_poste(id: int, db: Session = Depends(get_db)):
    poste = db.query(Poste).filter(Poste.id == id).first()
    if poste:
        db.delete(poste)
        db.commit()
    return RedirectResponse(url="/postes", status_code=303)
