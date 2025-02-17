from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter,Request

router = APIRouter()
base_dir = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(base_dir / "app/templates"))

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})