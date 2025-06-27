from fastapi import FastAPI

from app.utils.lifespan import lifespan
from app.routers import router as api_router

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")

@app.middleware("http")
async def log_timing(request, call_next):
    import time
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.url.path} took {duration:.2f}s")
    return response