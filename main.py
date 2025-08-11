import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine, get_db
from app.controllers import (
    auth_controller,
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
    homeController,
)
from fastapi import Request
from app.models.departement import Departement
from sqlalchemy.orm import Session

# Création de l'application FastAPI
template_dir = Path(__file__).resolve().parent / "templates"
static_dir = Path(__file__).resolve().parent / "resources"
app = FastAPI()

@app.middleware("http")
async def attach_current_departement(request: Request, call_next):
    # On récupère l'ID stocké en session
    departement_id = request.session.get("departement_id")
    request.state.current_dept = None
    if departement_id:
        # Ouvrir une session manuelle
        with engine.connect() as conn:
            session = Session(bind=conn)
            dpt = session.get(Departement, departement_id)
            request.state.current_dept = dpt
            session.close()
    response = await call_next(request)
    return response

# Middleware de session pour l'authentification
tmp_secret = os.getenv("SECRET_KEY", "change_me_to_a_strong_random_value")
app.add_middleware(
    SessionMiddleware,
    secret_key=tmp_secret,
    session_cookie="session",
)

# Mount du répertoire static
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount(
    "/static", StaticFiles(directory=os.path.join(BASE_DIR, "app/resources")), name="static"
)

# Configuration des templates Jinja2
templates = Jinja2Templates(directory="app/templates")

# Initialisation de la base de données (création des tables)
Base.metadata.create_all(bind=engine)

# Inclusion des routes
enable_routers = [
    auth_controller.router,
    departementController.router,
    gradeController.router,
    posteController.router,
    gradeParPosteController.router,
    employeController.router,
    affectationController.router,
    employeGradeController.router,
    tourController.router,
    remplacementController.router,
    permanenceController.router,
    homeController.router,
]
for router in enable_routers:
    app.include_router(router)

# Route d'accueil (redirection vers la page de login)
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return RedirectResponse(url="/accueil")
