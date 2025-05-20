import numpy as np
import pandas as pd
from datetime import datetime
from scipy.optimize import newton

def generate_cashflows(face: float, coupon_rate: float, frequency: int,
                       issue_date: datetime, maturity_date: datetime):
    periods = int((maturity_date.year - issue_date.year) * frequency)
    cf_dates = pd.date_range(start=issue_date, periods=periods+1, freq=f'{12//frequency}M')[1:]
    coupon = face * coupon_rate / frequency
    cashflows = [(d.date(), coupon) for d in cf_dates[:-1]]
    cashflows.append((cf_dates[-1].date(), coupon + face))
    return cashflows

def calculate_ytm(cashflows, clean_price: float, face: float, frequency: int):
    def price_for_y(y):
        return sum(cf[1] / (1 + y/frequency)**((i+1)) for i, cf in enumerate(cashflows)) - clean_price
    ytm = newton(price_for_y, 0.05)
    return ytm

def calculate_duration_convexity(cashflows, ytm: float, frequency: int):
    df = [(cf[1] / (1 + ytm/frequency)**((i+1))) for i, cf in enumerate(cashflows)]
    times = [(i+1)/frequency for i in range(len(cashflows))]
    pv = sum(df)
    macaulay = sum(t * pv_i for t, pv_i in zip(times, df)) / pv
    modified = macaulay / (1 + ytm/frequency)
    convexity = sum(t*(t+1/frequency) * pv_i for t, pv_i in zip(times, df)) / (pv*(1+ytm/frequency)**2)
    return macaulay, modified, convexity

def calculate_dv01(cashflows, ytm: float, frequency: int, clean_price: float):
    bumped_price = calculate_price(cashflows, ytm + 0.0001, frequency)
    dv01 = (bumped_price - clean_price) / 0.0001
    return abs(dv01)


def calculate_price(cashflows, ytm: float, frequency: int):
    return sum(cf[1] / (1 + ytm/frequency)**((i+1)) for i, cf in enumerate(cashflows))
