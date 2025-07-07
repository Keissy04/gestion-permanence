from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tour import Tour

router = APIRouter(tags=["Tours HTML"])
templates = Jinja2Templates(directory="app/templates")

# Liste
@router.get("/tours", response_class=HTMLResponse)
def list_tours(request: Request, db: Session = Depends(get_db)):
    tours = db.query(Tour).all()
    return templates.TemplateResponse("views/tour/index.html", {
        "request": request,
        "tours": tours
    })

# Formulaire création
@router.get("/tours/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("views/tour/create.html", {
        "request": request,
        "error": ""
    })

# Traitement création
@router.post("/tours/create")
def create_tour(request: Request, nom: str = Form(...), db: Session = Depends(get_db)):
    existing = db.query(Tour).filter(Tour.nom == nom).first()
    if existing:
        return templates.TemplateResponse("views/tour/create.html", {
            "request": request,
            "error": "Ce tour existe déjà"
        })
    tour = Tour(nom=nom)
    db.add(tour)
    db.commit()
    return RedirectResponse(url="/tours", status_code=303)

# Formulaire modification
@router.get("/tours/edit/{id}", response_class=HTMLResponse)
def edit_form(id: int, request: Request, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == id).first()
    return templates.TemplateResponse("views/tour/edit.html", {
        "request": request,
        "tour": tour,
        "error": ""
    })

# Traitement modification
@router.post("/tours/edit/{id}")
def update_tour(id: int, nom: str = Form(...), db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == id).first()
    if tour:
        tour.nom = nom
        db.commit()
    return RedirectResponse(url="/tours", status_code=303)

# Suppression
@router.get("/tours/delete/{id}")
def delete_tour(id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).filter(Tour.id == id).first()
    if tour:
        db.delete(tour)
        db.commit()
    return RedirectResponse(url="/tours", status_code=303)
