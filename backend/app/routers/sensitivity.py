
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import date

from app.services.sensitivity import shock_sensitivities

router = APIRouter(prefix="/sensitivity", tags=["Sensitivity"])

class BondInput(BaseModel):
    face: float
    issue_date: date
    maturity_date: date
    coupon_rate: float
    frequency: int
    clean_price: float

class ShockInput(BaseModel):
    bond: BondInput
    shocks_bp: List[float] = Field(..., description="Lista de shocks paralelos en basis points, e.g. [-100, -50, 0, 50, 100]")

class SensitivityOutput(BaseModel):
    shock_bp: float
    yield_: float = Field(..., alias="yield")
    price: float
    dv01: float

@router.post("/bond", response_model=List[SensitivityOutput])
async def bond_sensitivity(input: ShockInput):
    """
    Aplica shocks paralelos al yield de un bono y devuelve precio y DV01 para cada shock.
    """
    try:
        sens = shock_sensitivities(
            input.bond.face,
            input.bond.coupon_rate,
            input.bond.frequency,
            input.bond.issue_date,
            input.bond.maturity_date,
            input.bond.clean_price,
            input.shocks_bp
        )
        return sens
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculando sensibilidades: {e}")
