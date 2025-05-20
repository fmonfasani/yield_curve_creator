import os
import numpy as np
from scipy.optimize import newton, least_squares

from datetime import date
from typing import List

# Para generar flujos, reutilizamos tu servicio de cálculos
from app.services.calculations import generate_cashflows

BASE_DIR = os.getcwd()
RESULTS_DIR = os.path.join(BASE_DIR, "data", "results")


def bootstrap_spot_curve(bonds: List) -> (List[float], List[float]):
    """
    Dados una lista de objetos BondCurveInput con atributos:
      - issue_date (date)
      - maturity_date (date)
      - coupon_rate (float)
      - frequency (int)
      - clean_price (float)
    Devuelve:
      - times: lista de tiempos (años) de cada punto bootstrapped
      - rates: lista de tasas spot continuas bootstrapped

    Usa bootstrapping con descuento continuo.
    """
    # Ordenar bonos por maturity_date
    sorted_bonds = sorted(bonds, key=lambda b: b.maturity_date)
    known_times = []
    known_rates = []

    for bond in sorted_bonds:
        # Generar flujos con fechas
        cf = generate_cashflows(
            bond.face, bond.coupon_rate, bond.frequency,
            bond.issue_date, bond.maturity_date
        )
        # Calcular tiempos en años desde issue_date
        times = np.array([(d - bond.issue_date).days / 365.0 for d, _ in cf])
        amounts = np.array([a for _, a in cf])
        P = bond.clean_price

        # PV de flujos previos con tasas conocidas
        sum_prev = 0.0
        if known_times:
            for t_k, r_k in zip(known_times, known_rates):
                # encontrar índice del flujo en ese tiempo
                idx = np.where(np.isclose(times, t_k))[0]
                if idx.size:
                    sum_prev += amounts[idx[0]] * np.exp(-r_k * t_k)
        
        # Resolver tasa spot para el último flujo
        t_last = times[-1]
        a_last = amounts[-1]
        def f(r):
            return sum_prev + a_last * np.exp(-r * t_last) - P

        # Usar coupon_rate como semilla
        r_n = newton(f, bond.coupon_rate)

        known_times.append(t_last)
        known_rates.append(r_n)

    return known_times, known_rates


def nelson_siegel_curve(params, t):
    """
    Modelo Nelson-Siegel: r(t) = beta0 + beta1 * ((1 - exp(-t/tau)) / (t/tau))
                               + beta2 * (((1 - exp(-t/tau)) / (t/tau)) - exp(-t/tau))
    """
    beta0, beta1, beta2, tau = params
    t = np.array(t)
    with np.errstate(divide='ignore', invalid='ignore'):
        factor = (1 - np.exp(-t / tau)) / (t / tau)
        return beta0 + beta1 * factor + beta2 * (factor - np.exp(-t / tau))


def fit_nelson_siegel(times: List[float], rates: List[float]) -> (float, float, float, float):
    """
    Ajusta parámetros NS a los puntos de curva spot.
    Devuelve beta0, beta1, beta2, tau.
    """
    def residuals(params):
        return nelson_siegel_curve(params, times) - np.array(rates)

    # Guess inicial: nivel ~= última tasa, otros pequeños
    x0 = np.array([rates[-1], -0.02, 0.02, 1.0])
    # Bound tau > 0
    bounds = ([-np.inf, -np.inf, -np.inf, 0.01], [np.inf, np.inf, np.inf, 10.0])

    res = least_squares(residuals, x0, bounds=bounds)
    beta0, beta1, beta2, tau = res.x
    return beta0, beta1, beta2, tau
