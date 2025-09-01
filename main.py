import os
import uuid
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.orm import Session
from app.database import Base, engine
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
    remplacantController,
)
from app.models.departement import Departement

# Création de l'application FastAPI
template_dir = Path(__file__).resolve().parent / "templates"
static_dir = Path(__file__).resolve().parent / "resources"
app = FastAPI()

# Identifiant de démarrage (change à chaque démarrage)
app.state.boot_id = uuid.uuid4().hex

# Middleware d'attachement du département courant + invalidation si boot_id différent
@app.middleware("http")
async def attach_current_departement(request: Request, call_next):
    # Invalidation de session si le serveur a redémarré
    if request.session.get("boot_id") != request.app.state.boot_id:
        request.session.clear()

    # On récupère l'ID stocké en session
    departement_id = request.session.get("departement_id")
    request.state.current_dept = None
    if departement_id:
        # Ouvrir une session manuelle
        with engine.connect() as conn:
            session = Session(bind=conn)
            try:
                dpt = session.get(Departement, departement_id)
                request.state.current_dept = dpt
            finally:
                session.close()

    response = await call_next(request)
    return response

# Middleware de session pour l'authentification
tmp_secret = os.getenv("SECRET_KEY", "change_me_to_a_strong_random_value")
app.add_middleware(
    SessionMiddleware,
    secret_key=tmp_secret,
    session_cookie="session",
    # max_age=3600,  # (optionnel) TTL cookie 1h
)

# Mount du répertoire static
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount(
    "/static", StaticFiles(directory=os.path.join(BASE_DIR, "app/resources")), name="static"
)

# Templates Jinja2
templates = Jinja2Templates(directory="app/templates")

# Initialisation DB
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
    remplacantController.router,
]
for router in enable_routers:
    app.include_router(router)

# Route d'accueil
@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return RedirectResponse(url="/accueil")

# <script>
#     // Export pdf
#            // Add click event listener to the export button
#            document.addEventListener('DOMContentLoaded', function() {
#                var exportPdf = html2pdf();
#                var exportButton = document.getElementById('exportButton');
#                var chartCanvas = document.getElementById('card-body');

#                var exportToPdf = function() {
#                    exportPdf.set({
#                        margin: [10, 10, 10, 10],
#                        filename: 'facture.pdf',
#                        image: { type: 'jpeg', quality: 0.98 },
#                        html2canvas: { scale: 2 },
#                        jsPDF: { unit: 'mm', format: 'a4', orientation: 'paysage'}
#                    });

#                    exportPdf.from(chartCanvas).save();
#                };
#                exportButton.addEventListener('click', exportToPdf);
#            });
#    </script>