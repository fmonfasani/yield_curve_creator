from datetime import datetime


def parse_prospect(path: str) -> dict:
    """
    Stub temporal: devuelve valores hardcodeados para testing.
    En producción, reemplaza con lógica de extracción de PDF/Word.
    """
    return {
        "face": 1000.0,
        "coupon_rate": 0.05,
        "frequency": 2,
        "issue_date": datetime(2020, 1, 1),
        "maturity_date": datetime(2025, 1, 1),
        "clean_price": 980.0,
    }
