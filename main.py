from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Sert les fichiers statiques
app.mount("/static", StaticFiles(directory="app/resources"), name="static")

# Configure les templates
templates = Jinja2Templates(directory="app/templates")

# Page d'accueil (démarrage)
@app.get("/", response_class=HTMLResponse)
def accueil(request: Request):
    return templates.TemplateResponse("views/layout/table.html", {"request": request})