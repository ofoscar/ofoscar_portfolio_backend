from fastapi import FastAPI

from ofoscar_backend.routers.auth import router as auth_router
from ofoscar_backend.routers.projects import router as projects_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(projects_router)