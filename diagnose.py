"""Diagnose a company using the temporal pipe graph."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "diagnosis.db"


def _db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def add_pipe(company_id, description, stack=None, site=None, parent_id=None):
    """Add a pipe node (topology). Returns pipe id."""
    db = _db()
    depth = 0
    if parent_id is not None:
        row = db.execute("SELECT depth FROM pipe WHERE id = ?", (parent_id,)).fetchone()
        if row:
            depth = row["depth"] + 1
    cur = db.execute(
        "INSERT INTO pipe (company_id, parent_id, description, stack, site, depth) VALUES (?, ?, ?, ?, ?, ?)",
        (company_id, parent_id, description, stack, site, depth),
    )
    db.commit()
    pid = cur.lastrowid
    db.close()
    return pid


def add_event(pipe_id, source_date, status, evidence, source_url):
    """Record an event — a public record that changes a pipe's state."""
    db = _db()
    cur = db.execute(
        "INSERT INTO event (pipe_id, source_date, status, evidence, source_url) VALUES (?, ?, ?, ?, ?)",
        (pipe_id, source_date, status, evidence, source_url),
    )
    db.commit()
    eid = cur.lastrowid
    db.close()
    return eid


def add_prediction(
    company_id, pipe_id, pred_type, category, direction,
    catalyst, resolution_source, window_start, window_end,
    pass_condition, reasoning, run,
):
    """Record and publish a prediction. Sets published_at to now. Returns prediction id."""
    db = _db()
    cur = db.execute(
        "INSERT INTO prediction (company_id, pipe_id, type, category, direction, "
        "catalyst, resolution_source, window_start, window_end, pass_condition, "
        "reasoning, run, published_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))",
        (company_id, pipe_id, pred_type, category, direction,
         catalyst, resolution_source, window_start, window_end,
         pass_condition, reasoning, run),
    )
    db.commit()
    pid = cur.lastrowid
    db.close()
    return pid


def add_analyst_call(prediction_id, analyst_name, direction, source_url=None, call_date=None):
    """Record an analyst's position. One per prediction (UNIQUE constraint)."""
    db = _db()
    cur = db.execute(
        "INSERT INTO analyst_call (prediction_id, analyst_name, direction, source_url, call_date) VALUES (?, ?, ?, ?, ?)",
        (prediction_id, analyst_name, direction, source_url, call_date),
    )
    db.commit()
    cid = cur.lastrowid
    db.close()
    return cid


def score_prediction(prediction_id, outcome, notes=None):
    """Score a prediction after catalyst date."""
    db = _db()
    db.execute(
        "UPDATE prediction SET outcome = ?, outcome_notes = ?, outcome_date = datetime('now') WHERE id = ?",
        (outcome, notes, prediction_id),
    )
    db.commit()
    db.close()


def show_timeline(company_id):
    """Print the event timeline for a company — the temporal graph as it developed."""
    db = _db()

    pipes = db.execute(
        "SELECT id, description, stack, site, depth FROM pipe WHERE company_id = ? ORDER BY depth, id",
        (company_id,),
    ).fetchall()

    if not pipes:
        print("No pipes for this company.")
        return

    for pipe in pipes:
        events = db.execute(
            "SELECT source_date, status, evidence, source_url FROM event WHERE pipe_id = ? ORDER BY source_date",
            (pipe["id"],),
        ).fetchall()

        indent = "  " * pipe["depth"]
        tag = f"[{pipe['stack'][0]}]" if pipe["stack"] else "   "
        desc = pipe["description"][:50]
        print(f"{indent}{tag} {desc}")

        if not events:
            print(f"{indent}    (no events)")
        else:
            for e in events:
                markers = {"functional": "✓", "broken": "✗", "stressed": "~", "repaired": "↑", "unknown": "?"}
                m = markers.get(e["status"], " ")
                print(f"{indent}    {e['source_date']}  {m} {e['status']:<10}  {e['evidence'][:60]}")

        print()

    db.close()


def show_transitions(company_id):
    """Show only pipes whose status changed — the interesting arcs."""
    db = _db()

    pipes = db.execute(
        "SELECT id, description, stack, site FROM pipe WHERE company_id = ? ORDER BY depth, id",
        (company_id,),
    ).fetchall()

    for pipe in pipes:
        events = db.execute(
            "SELECT source_date, status, evidence FROM event WHERE pipe_id = ? ORDER BY source_date",
            (pipe["id"],),
        ).fetchall()

        if len(events) < 2:
            continue

        transitions = []
        for i in range(1, len(events)):
            if events[i]["status"] != events[i - 1]["status"]:
                transitions.append(
                    f"  {events[i-1]['source_date']} {events[i-1]['status']} → {events[i]['source_date']} {events[i]['status']}"
                )

        if transitions:
            tag = f"[{pipe['stack'][0]}]" if pipe["stack"] else "   "
            print(f"{tag} {pipe['description']}")
            for t in transitions:
                print(t)
            print()

    db.close()


def show_scorecard():
    """Print the scorecard."""
    db = _db()
    rows = db.execute("SELECT * FROM scorecard").fetchall()
    if not rows:
        print("No predictions yet.")
        return
    for row in rows:
        print("---")
        for key in row.keys():
            if row[key] is not None:
                print(f"  {key}: {row[key]}")
    db.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: diagnose.py [timeline TICKER | transitions TICKER | scorecard]")
        sys.exit(1)

    cmd = sys.argv[1]
    db = _db()

    if cmd in ("timeline", "transitions") and len(sys.argv) >= 3:
        row = db.execute("SELECT id FROM company WHERE ticker = ?", (sys.argv[2].upper(),)).fetchone()
        db.close()
        if not row:
            print(f"Company {sys.argv[2]} not found.")
            sys.exit(1)
        if cmd == "timeline":
            show_timeline(row["id"])
        else:
            show_transitions(row["id"])
    elif cmd == "scorecard":
        db.close()
        show_scorecard()
    else:
        db.close()
        print("Usage: diagnose.py [timeline TICKER | transitions TICKER | scorecard]")
