from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.departement import Departement
from app.utils.security import verify_password

router = APIRouter(tags=["Authentification HTML"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request, error: Optional[str] = None):
    # Déjà connecté ? on redirige
    if request.session.get("departement_id"):
        return RedirectResponse(url="/departements", status_code=303)
    return templates.TemplateResponse("views/auth/login.html", {"request": request, "error": error})

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    mdp: str = Form(...),
    db: Session = Depends(get_db)
):
    dpt = db.query(Departement).filter(Departement.email == email).first()
    if not dpt or not verify_password(mdp, dpt.mdp):
        return templates.TemplateResponse("views/auth/login.html", {
            "request": request,
            "error": "Email ou mot de passe invalide."
        })

    # Authentifié ⇒ on stocke l'id + le boot_id courant pour invalider à chaque reboot
    request.session["departement_id"] = dpt.id
    request.session["boot_id"] = request.app.state.boot_id

    return RedirectResponse(url="/departements", status_code=303)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
