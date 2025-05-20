from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, condecimal
from datetime import date
from app.services.calculations import (
    generate_cashflows, calculate_ytm,
    calculate_duration_convexity, calculate_dv01
)

router = APIRouter(prefix="/calculate", tags=["Calculations"])

class BondInput(BaseModel):
    face: condecimal(gt=0)
    coupon_rate: condecimal(ge=0, le=1)
    frequency: int
    issue_date: date
    maturity_date: date
    clean_price: float

@router.post("/")
def compute(bond: BondInput):
    cashflows = generate_cashflows(
        float(bond.face), float(bond.coupon_rate), bond.frequency,
        bond.issue_date, bond.maturity_date
    )
    ytm = calculate_ytm(cashflows, bond.clean_price, bond.face, bond.frequency)
    macaulay, modified, convexity = calculate_duration_convexity(cashflows, ytm, bond.frequency)
    dv01 = calculate_dv01(cashflows, ytm, bond.frequency, bond.clean_price)
    return {
        "cashflows": [{"date": str(d), "amount": amt} for d, amt in cashflows],
        "ytm": ytm,
        "duration_macaulay": macaulay,
        "duration_modified": modified,
        "convexity": convexity,
        "dv01": dv01
    }
