from fastapi import FastAPI
from app.routes import tasks,users,home
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )
# Include routers
app.include_router(home.router)
app.include_router(users.router,prefix="/users")
app.include_router(tasks.router,prefix="/tasks")
