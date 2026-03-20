"""Diagnose a company by building the recursive pipe tree."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "diagnosis.db"


def add_pipe(
    company_id: int,
    description: str,
    stack: str | None = None,
    site: str | None = None,
    parent_id: int | None = None,
) -> int:
    """Add a pipe node to the tree. Returns the pipe id."""
    db = sqlite3.connect(DB_PATH)
    depth = 0
    if parent_id is not None:
        parent_depth = db.execute(
            "SELECT depth FROM pipe WHERE id = ?", (parent_id,)
        ).fetchone()
        if parent_depth:
            depth = parent_depth[0] + 1

    cur = db.execute(
        "INSERT INTO pipe (company_id, parent_id, description, stack, site, depth) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (company_id, parent_id, description, stack, site, depth),
    )
    db.commit()
    pipe_id = cur.lastrowid
    db.close()
    return pipe_id


def diagnose_pipe(pipe_id: int, diagnosis: str, status: str = "diagnosed"):
    """Record a diagnosis on a pipe node."""
    db = sqlite3.connect(DB_PATH)
    db.execute(
        "UPDATE pipe SET diagnosis = ?, status = ? WHERE id = ?",
        (diagnosis, status, pipe_id),
    )
    db.commit()
    db.close()


def add_prediction(
    company_id: int,
    pipe_id: int | None,
    pred_type: str,
    claim: str,
    evidence: str | None = None,
    catalyst_date: str | None = None,
    timeframe: str | None = None,
) -> int:
    """Record a prediction. Returns prediction id."""
    db = sqlite3.connect(DB_PATH)
    cur = db.execute(
        "INSERT INTO prediction (company_id, pipe_id, type, claim, evidence, catalyst_date, timeframe) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (company_id, pipe_id, pred_type, claim, evidence, catalyst_date, timeframe),
    )
    db.commit()
    pred_id = cur.lastrowid
    db.close()
    return pred_id


def add_analyst_call(
    prediction_id: int,
    analyst_name: str,
    position: str,
    source_url: str | None = None,
    call_date: str | None = None,
) -> int:
    """Record an analyst's position for head-to-head comparison."""
    db = sqlite3.connect(DB_PATH)
    cur = db.execute(
        "INSERT INTO analyst_call (prediction_id, analyst_name, position, source_url, call_date) "
        "VALUES (?, ?, ?, ?, ?)",
        (prediction_id, analyst_name, position, source_url, call_date),
    )
    db.commit()
    call_id = cur.lastrowid
    db.close()
    return call_id


def score_prediction(prediction_id: int, outcome: str, notes: str | None = None):
    """Score a prediction after the catalyst date."""
    db = sqlite3.connect(DB_PATH)
    db.execute(
        "UPDATE prediction SET outcome = ?, outcome_notes = ?, outcome_date = datetime('now') WHERE id = ?",
        (outcome, notes, prediction_id),
    )
    db.commit()
    db.close()


def show_tree(company_id: int):
    """Print the pipe tree for a company."""
    db = sqlite3.connect(DB_PATH)
    rows = db.execute(
        "SELECT id, parent_id, depth, description, stack, site, status, diagnosis "
        "FROM pipe WHERE company_id = ? ORDER BY depth, id",
        (company_id,),
    ).fetchall()

    if not rows:
        print("No pipes for this company.")
        return

    for pipe_id, parent_id, depth, desc, stack, site, status, diagnosis in rows:
        indent = "  " * depth
        label = desc
        if stack:
            label += f" [{stack}]"
        if site:
            label += f" ({site})"
        status_marker = {"unexplored": "?", "claimed": "~", "diagnosed": "!", "cleared": "✓"}
        marker = status_marker.get(status, "?")
        line = f"{indent}{marker} {label}"
        if diagnosis:
            line += f" → {diagnosis}"
        print(line)

    db.close()


def show_scorecard():
    """Print the scorecard."""
    db = sqlite3.connect(DB_PATH)
    rows = db.execute("SELECT * FROM scorecard").fetchall()
    if not rows:
        print("No predictions yet.")
        return

    cols = [d[0] for d in db.execute("SELECT * FROM scorecard LIMIT 0").description]
    for row in rows:
        print("---")
        for col, val in zip(cols, row):
            if val is not None:
                print(f"  {col}: {val}")
    db.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: diagnose.py [tree TICKER | scorecard]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "tree" and len(sys.argv) >= 3:
        db = sqlite3.connect(DB_PATH)
        row = db.execute("SELECT id FROM company WHERE ticker = ?", (sys.argv[2].upper(),)).fetchone()
        db.close()
        if row:
            show_tree(row[0])
        else:
            print(f"Company {sys.argv[2]} not found.")
    elif cmd == "scorecard":
        show_scorecard()
    else:
        print("Usage: diagnose.py [tree TICKER | scorecard]")
