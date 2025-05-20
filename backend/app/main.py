from fastapi import FastAPI
from app.routers import prospect, calculations, jobs



app = FastAPI(
    title="Yield Curve Creator API",
    version="0.1.0",
    description="API para parsing de prospectos y cálculos de bonos"
)

app.include_router(prospect.router)
app.include_router(calculations.router)
app.include_router(jobs.router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a Yield Curve Creator API!"}