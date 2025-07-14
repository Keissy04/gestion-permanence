from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

from app.database import Base, engine
from app.controllers import (
    departementController,
    gradeController,
    posteController,
    gradeParPosteController,
    employeController,
    affectationController,
    employeGradeController,
    tourController,
    remplacementController,
    permanenceController,
)

app = FastAPI()

# ✅ Correction du chemin ABSOLU vers resources/
BASE_DIR = Path(__file__).resolve().parent.parent  # ← racine du projet
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app/resources")), name="static")

# Configure les templates
templates = Jinja2Templates(directory="app/templates")

# Crée les tables
Base.metadata.create_all(bind=engine)

# Routes
app.include_router(departementController.router)
app.include_router(gradeController.router)
app.include_router(posteController.router)
app.include_router(gradeParPosteController.router)
app.include_router(employeController.router)
app.include_router(affectationController.router)
app.include_router(employeGradeController.router)
app.include_router(tourController.router)
app.include_router(remplacementController.router)
app.include_router(permanenceController.router)

@app.get("/", response_class=HTMLResponse)
def accueil(request: Request):
    return templates.TemplateResponse("views/layout/table.html", {"request": request})
