from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employe import Employe

# test auth
from app.utils.auth import get_current_departement

router = APIRouter(tags=["Employés HTML"])
templates = Jinja2Templates(directory="app/templates")

# Liste
@router.get("/employes", response_class=HTMLResponse)
def list_employes(request: Request,
                  db: Session = Depends(get_db),
                  page: int = 1,
                  current_dpt = Depends(get_current_departement)):
    
    per_page = 5
    total = db.query(Employe).count()
    pages = (total + per_page - 1) // per_page
    employes = db.query(Employe).offset((page - 1) * per_page).limit(per_page).all()

    return templates.TemplateResponse("views/employe/index.html", {
        "request": request,
        "employes": employes,
        "page": page,
        "pages": pages,
        "departement": current_dpt
    })
# Création - formulaire
@router.get("/employes/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("views/employe/create.html", {"request": request, "error": ""})

# Création - traitement
@router.post("/employes/create")
def create_employe(request: Request, nom: str = Form(...), db: Session = Depends(get_db)):
    if not nom:
        return templates.TemplateResponse("views/employe/create.html", {"request": request, "error": "Le nom est requis."})
    employe = Employe(nom=nom)
    db.add(employe)
    db.commit()
    return RedirectResponse(url="/employes", status_code=303)

# Modification - formulaire
@router.get("/employes/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    employe = db.query(Employe).filter(Employe.id == id).first()
    if not employe:
        return RedirectResponse(url="/employes", status_code=303)
    return templates.TemplateResponse("views/employe/edit.html", {"request": request, "employe": employe, "error": ""})

# Modification - traitement
@router.post("/employes/edit/{id}")
def update_employe(id: int, request: Request, nom: str = Form(...), db: Session = Depends(get_db)):
    employe = db.query(Employe).filter(Employe.id == id).first()
    if employe:
        employe.nom = nom
        db.commit()
    return RedirectResponse(url="/employes", status_code=303)

# Suppression
@router.get("/employes/delete/{id}")
def delete_employe(id: int, db: Session = Depends(get_db)):
    employe = db.query(Employe).filter(Employe.id == id).first()
    if employe:
        db.delete(employe)
        db.commit()
    return RedirectResponse(url="/employes", status_code=303)
