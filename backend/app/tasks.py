from app.celery_app import celery
import os, json, tempfile
from datetime import datetime, date
from app.services.parsing import parse_prospect
from app.services.calculations import (
    generate_cashflows, calculate_ytm,
    calculate_duration_convexity, calculate_dv01
)

BASE_DIR = os.getcwd()
RESULTS_DIR = os.path.join(BASE_DIR, "data", "results")

@celery.task(name="app.tasks.process_prospect")
def process_prospect(job_id: str, filename: str):
    prospect_path = os.path.join(BASE_DIR, "data", "prospects", filename)
    bond_data = parse_prospect(prospect_path)

    # Serializar bond_data
    serializable = {}
    for k, v in bond_data.items():
        if isinstance(v, (datetime, date)):
            serializable[k] = v.isoformat()
        else:
            serializable[k] = v

    cf = generate_cashflows(
        bond_data["face"], bond_data["coupon_rate"],
        bond_data["frequency"], bond_data["issue_date"],
        bond_data["maturity_date"]
    )
    cashflows = [
        {"date": d.isoformat() if hasattr(d, "isoformat") else str(d), "amount": a}
        for d, a in cf
    ]
    ytm = calculate_ytm(cf, serializable["clean_price"], serializable["face"], serializable["frequency"])
    macaulay, modified, convexity = calculate_duration_convexity(cf, ytm, serializable["frequency"])
    dv01 = calculate_dv01(cf, ytm, serializable["frequency"], serializable["clean_price"])

    result = {
        **serializable,
        "cashflows": cashflows,
        "ytm": ytm,
        "duration_macaulay": macaulay,
        "duration_modified": modified,
        "convexity": convexity,
        "dv01": dv01
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    tmpf = tempfile.NamedTemporaryFile(delete=False, dir=RESULTS_DIR, suffix=".json.tmp", mode="w", encoding="utf-8")
    json.dump(result, tmpf, ensure_ascii=False, indent=2)
    tmpf.flush()
    tmp_path = tmpf.name
    tmpf.close()
    os.replace(tmp_path, os.path.join(RESULTS_DIR, f"{job_id}.json"))
