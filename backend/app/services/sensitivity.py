import numpy as np
from datetime import date
from typing import List, Tuple
from app.services.calculations import generate_cashflows, calculate_ytm


def calc_price_from_yield(cf: List[Tuple[float, float]], yield_rate: float) -> float:
    """
    Calcula el precio limpio de un bono dado su yield y flujos de caja descontados.
    cf: lista de (t_years, amount)
    yield_rate: tasa periódica equivalente
    """
    price = 0.0
    for t, a in cf:
        price += a / ((1 + yield_rate) ** t)
    return price


def shock_sensitivities(
    face: float,
    coupon_rate: float,
    frequency: int,
    issue_date: date,
    maturity_date: date,
    clean_price: float,
    shocks_bp: List[float]
) -> List[dict]:
    """
    Para cada shock en basis points aplica un shift paralelo al yield original,
    y recalcula el precio y el DV01 aproximado.
    """
    # 1) Obtener flujos en términos de (tiempo en años, monto)
    raw_cf = generate_cashflows(face, coupon_rate, frequency, issue_date, maturity_date)
    cf = []
    for dt, amt in raw_cf:
        # convertir fecha dt a años desde issue_date
        t = (dt - issue_date).days / 365.0
        cf.append((t, amt))

    # 2) Yield original
    ytm = calculate_ytm(cf, clean_price, face, frequency)
    
    # 3) Sensitivities
    sensitivities = []
    # Pre-calcular DV01 usando diferencial de 1bp
    dv01 = -(calc_price_from_yield(cf, ytm + 0.0001) - calc_price_from_yield(cf, ytm - 0.0001)) / 2

    for bp in shocks_bp:
        shift = bp / 10000  # de puntos base a tasa decimal
        y_new = ytm + shift
        price_new = calc_price_from_yield(cf, y_new)
        sensitivities.append({
            "shock_bp": bp,
            "yield": y_new,
            "price": price_new,
            "dv01": dv01
        })
    return sensitivities
