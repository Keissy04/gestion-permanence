from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.controllers import departementController
from app.controllers import gradeController
from app.controllers import posteController
from app.controllers import gradeParPosteController
from app.controllers import employeController
from app.controllers import affectationController
app = FastAPI()

# Sert les fichiers statiques
app.mount("/static", StaticFiles(directory="app/resources"), name="static")


# Configure les templates
templates = Jinja2Templates(directory="app/templates")

# Crée les tables en base de donnée
Base.metadata.create_all(bind=engine)

# Inclure les routes du CRUD 
app.include_router(departementController.router)
app.include_router(gradeController.router)
app.include_router(posteController.router)
app.include_router(gradeParPosteController.router)
app.include_router(employeController.router)
app.include_router(affectationController.router)

# Page d'accueil
@app.get("/", response_class=HTMLResponse)
def accueil(request: Request):
    return templates.TemplateResponse("views/layout/table.html", {"request": request})
