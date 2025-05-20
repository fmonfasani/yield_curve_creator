from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import date
from app.services.sensitivity import shock_sensitivities


from app.services.curve import bootstrap_spot_curve, fit_nelson_siegel

router = APIRouter(
    prefix="/curve",
    tags=["Curve"]
)

class BondCurveInput(BaseModel):
    face: float = Field(..., description="Face (nominal) value of the bond, e.g. 1000.0")
    issue_date: date
    maturity_date: date
    coupon_rate: float = Field(..., description="Annual coupon rate, e.g. 0.05 for 5%")
    frequency: int = Field(..., description="Number of coupon payments per year")
    clean_price: float = Field(..., description="Clean market price of the bond")

class SpotCurveOutput(BaseModel):
    times: List[float] = Field(..., description="Time to maturity in years for each bootstrapped point")
    rates: List[float] = Field(..., description="Bootstrapped zero rates for each point")

class NSFitOutput(BaseModel):
    beta0: float
    beta1: float
    beta2: float
    tau: float



class CurveResponse(BaseModel):
    spot_curve: SpotCurveOutput
    ns_fit: NSFitOutput
    forward_curve: List[float] = Field(..., description="Implied forward rates between bootstrapped points")

@router.post("/build", response_model=CurveResponse)
async def build_curve(bonds: List[BondCurveInput]):
    """
    Construye la curva spot por bootstrap y ajusta el modelo Nelson–Siegel.
    """
    if len(bonds) < 2:
        raise HTTPException(status_code=400, detail="Se requieren al menos dos bonos para el bootstrap de curva.")
    try:
        # Paso 1: Bootstrap de la curva spot
        times, rates = bootstrap_spot_curve(bonds)
        spot = SpotCurveOutput(times=times, rates=rates)
        # Paso 2: Ajuste Nelson–Siegel
        beta0, beta1, beta2, tau = fit_nelson_siegel(times, rates)
        ns = NSFitOutput(beta0=beta0, beta1=beta1, beta2=beta2, tau=tau)
        # Paso 3: Cálculo de tasas forward implícitas
        forward = []
        for i in range(len(times) - 1):
            fwd = ((1 + rates[i+1])**times[i+1] / (1 + rates[i])**times[i])**(1/(times[i+1] - times[i])) - 1
            forward.append(fwd)
        return CurveResponse(spot_curve=spot, ns_fit=ns, forward_curve=forward)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error construyendo curva: {e}")
