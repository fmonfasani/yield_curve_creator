from fastapi import FastAPI
from app.routers import prospect, calculations, jobs
from app.routers.curve import router as curve_router
from app.routers.sensitivity import router as sens_router


app = FastAPI(
    title="Yield Curve Creator API",
    version="0.1.0",
    description="API para parsing de prospectos y cálculos de bonos"
)

app.include_router(prospect.router)
app.include_router(calculations.router)
app.include_router(jobs.router)
app.include_router(curve_router)
app.include_router(sens_router)



@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a Yield Curve Creator API!"}