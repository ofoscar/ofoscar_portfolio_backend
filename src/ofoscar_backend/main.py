from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ofoscar_backend.routers.auth import router as auth_router
from ofoscar_backend.routers.projects import router as projects_router
from ofoscar_backend.routers.uploads import router as uploads_router
from ofoscar_backend.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(uploads_router)