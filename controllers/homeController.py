from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Accueil HTML"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/accueil", response_class=HTMLResponse)
def accueil(request: Request):
    return templates.TemplateResponse("views/home/accueil.html", {"request": request})
