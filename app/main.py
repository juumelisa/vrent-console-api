from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config.database import Base, engine
from app.src.admin import router as adminRouter
from app.src.auth import router as authRouter
from app.src.vehicles import router as vehiclesRouter
import os

if os.getenv("ENV") == "local":
    Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(adminRouter.router)
app.include_router(authRouter.router)
app.include_router(vehiclesRouter.router)

@app.exception_handler(401)
async def api_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=200,
        content=exc.detail
    )