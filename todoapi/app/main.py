from fastapi import FastAPI
from app.routes import tasks,users,home

app = FastAPI()

# Include routers
app.include_router(home.router)
app.include_router(users.router,prefix="/users")
app.include_router(tasks.router,prefix="/tasks")
