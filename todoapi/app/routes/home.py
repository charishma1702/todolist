from pathlib import Path
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.utils.utils import verify_password, create_access_token, decode_access_token
from app.database.db import Users_Collection
from app.models.models import LoginRequest


router = APIRouter()

# Define the base directory for template rendering
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "app/templates"))

# Route for rendering the login page
@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(payload: LoginRequest):
    user = Users_Collection.find_one({"email": payload.email})
    # Check if user exists
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    # Verify hashed password
    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")  

    # Generate JWT Token if credentials are correct
    access_token = create_access_token(data={"email": user["email"], "password":user['password']})
    email=user.get("email")
    fullname = user.get("name", "")
    firstname = fullname.split()[0] 

    response = JSONResponse(content={"message": "Login successful", "firstname":firstname, "token": access_token, "email":email})

    # Set the JWT token as an HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Prevent JavaScript access for security
        secure=True,  # Ensure HTTPS is used
        samesite="Lax",  # Prevent CSRF attacks
        max_age=900  # 15 minutes (same as token expiration)
    )
    return response

@router.get("/protected")
async def protected_route(token_data: dict = Depends(decode_access_token)):
    return {"message": "You are authenticated", "user": token_data}


# Route for rendering the registration page
@router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Route for rendering the index (dashboard) page
@router.get("/index")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/profile")
async def profile(request:Request):
    return templates.TemplateResponse("profile.html", {"request": request})
