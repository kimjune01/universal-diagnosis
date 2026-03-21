"""FastAPI backend for the diagnosis viewer."""

import math
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

DB_PATH = Path(__file__).parent / "diagnosis.db"

app = FastAPI(title="Universal Diagnosis")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def _db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db


@app.get("/api/companies")
def list_companies():
    db = _db()
    rows = db.execute("""
        SELECT
            c.id, c.ticker, c.name,
            p.category, p.direction, p.outcome,
            (SELECT count(*) FROM event e JOIN pipe pi ON e.pipe_id = pi.id WHERE pi.company_id = c.id) AS event_count
        FROM company c
        LEFT JOIN prediction p ON p.company_id = c.id AND p.published_at IS NOT NULL
        ORDER BY p.run, c.ticker
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@app.get("/api/companies/{ticker}")
def get_company(ticker: str):
    db = _db()
    company = db.execute("SELECT * FROM company WHERE ticker = ?", (ticker.upper(),)).fetchone()
    if not company:
        db.close()
        raise HTTPException(404, f"Company {ticker} not found")

    cid = company["id"]

    pipes = db.execute(
        "SELECT id, description, stack, site, depth FROM pipe WHERE company_id = ? ORDER BY depth, id",
        (cid,),
    ).fetchall()

    events = db.execute("""
        SELECT e.id, e.pipe_id, pi.site AS pipe_site, pi.stack AS pipe_stack,
               e.source_date, e.status, e.evidence, e.source_url
        FROM event e
        JOIN pipe pi ON e.pipe_id = pi.id
        WHERE pi.company_id = ?
        ORDER BY e.source_date ASC, e.id ASC
    """, (cid,)).fetchall()

    prediction = db.execute("""
        SELECT id, arm, category, direction, catalyst, resolution_source,
               window_start, window_end, pass_condition, reasoning, run, outcome
        FROM prediction WHERE company_id = ? AND arm = 'temporal' AND published_at IS NOT NULL
        LIMIT 1
    """, (cid,)).fetchone()

    analyst = db.execute("""
        SELECT direction, catalyst, reasoning, outcome
        FROM prediction WHERE company_id = ? AND arm = 'analyst' AND published_at IS NOT NULL
        LIMIT 1
    """, (cid,)).fetchone() if prediction else None

    financials = db.execute("""
        SELECT cash, quarterly_burn, source_date, source_url
        FROM financial_snapshot WHERE company_id = ?
        ORDER BY source_date DESC LIMIT 1
    """, (cid,)).fetchone()

    db.close()

    fin = None
    if financials:
        cash = financials["cash"]
        burn = financials["quarterly_burn"]
        runway_quarters = round(cash / burn, 1) if burn > 0 else None
        fin = {**dict(financials), "runway_quarters": runway_quarters, "runway_months": round(runway_quarters * 3) if runway_quarters else None}

    return {
        "ticker": company["ticker"],
        "name": company["name"],
        "pipes": [dict(p) for p in pipes],
        "events": [dict(e) for e in events],
        "prediction": dict(prediction) if prediction else None,
        "analyst": dict(analyst) if analyst else None,
        "financials": fin,
    }


@app.get("/api/predictions")
def list_predictions():
    db = _db()
    rows = db.execute("""
        SELECT
            p.id, c.ticker, c.name AS company_name,
            p.arm, p.category, p.direction, p.catalyst, p.window_start, p.window_end,
            p.pass_condition, p.reasoning, p.run, p.published_at, p.outcome
        FROM prediction p
        JOIN company c ON c.id = p.company_id
        WHERE p.published_at IS NOT NULL
        ORDER BY p.window_end
    """).fetchall()
    db.close()
    return [dict(r) for r in rows]


@app.get("/api/stats")
def get_stats():
    db = _db()
    rows = db.execute("""
        SELECT outcome FROM prediction WHERE published_at IS NOT NULL
    """).fetchall()
    db.close()

    outcomes = [r["outcome"] for r in rows]
    n = len(outcomes)
    hits = outcomes.count("hit")
    misses = outcomes.count("miss")
    pending = outcomes.count("pending")
    resolved = hits + misses

    accuracy = round(hits / resolved, 4) if resolved > 0 else None

    # Binomial p-value (one-sided, normal approx)
    p_value = None
    if resolved > 0:
        p0 = 0.5
        p_hat = hits / resolved
        se = math.sqrt(p0 * (1 - p0) / resolved) if resolved > 0 else 0
        if se > 0:
            z = (p_hat - p0) / se
            p_value = round(0.5 * (1 - math.erf(z / math.sqrt(2))), 4)

    return {
        "n": n,
        "resolved": resolved,
        "hits": hits,
        "misses": misses,
        "pending": pending,
        "accuracy": accuracy,
        "p_value": p_value,
        "base_rate": 0.5,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
