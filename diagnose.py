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


def add_snapshot(company_id, label, timestamp):
    """Add a temporal snapshot. Returns snapshot id."""
    db = _db()
    cur = db.execute(
        "INSERT INTO snapshot (company_id, label, timestamp) VALUES (?, ?, ?)",
        (company_id, label, timestamp),
    )
    db.commit()
    sid = cur.lastrowid
    db.close()
    return sid


def set_state(pipe_id, snapshot_id, status, evidence=None, source_url=None):
    """Record a pipe's state at a snapshot. Upserts."""
    db = _db()
    db.execute(
        "INSERT INTO pipe_state (pipe_id, snapshot_id, status, evidence, source_url) "
        "VALUES (?, ?, ?, ?, ?) "
        "ON CONFLICT(pipe_id, snapshot_id) DO UPDATE SET status=excluded.status, evidence=excluded.evidence, source_url=excluded.source_url",
        (pipe_id, snapshot_id, status, evidence, source_url),
    )
    db.commit()
    db.close()


def add_prediction(company_id, pipe_id, pred_type, claim, evidence=None, catalyst_date=None, timeframe=None):
    """Record a prediction. Returns prediction id."""
    db = _db()
    cur = db.execute(
        "INSERT INTO prediction (company_id, pipe_id, type, claim, evidence, catalyst_date, timeframe) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (company_id, pipe_id, pred_type, claim, evidence, catalyst_date, timeframe),
    )
    db.commit()
    pid = cur.lastrowid
    db.close()
    return pid


def add_analyst_call(prediction_id, analyst_name, position, source_url=None, call_date=None):
    """Record an analyst's position."""
    db = _db()
    cur = db.execute(
        "INSERT INTO analyst_call (prediction_id, analyst_name, position, source_url, call_date) VALUES (?, ?, ?, ?, ?)",
        (prediction_id, analyst_name, position, source_url, call_date),
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


def show_temporal(company_id):
    """Print the temporal graph: pipe states across snapshots."""
    db = _db()

    snapshots = db.execute(
        "SELECT id, label, date_start, date_end FROM snapshot WHERE company_id = ? ORDER BY date_start",
        (company_id,),
    ).fetchall()

    pipes = db.execute(
        "SELECT id, description, stack, site, depth FROM pipe WHERE company_id = ? ORDER BY depth, id",
        (company_id,),
    ).fetchall()

    if not pipes:
        print("No pipes for this company.")
        return
    if not snapshots:
        print("No snapshots for this company.")
        return

    # Header
    snap_labels = [s["label"] for s in snapshots]
    col_w = max(len(l) for l in snap_labels) + 2
    pipe_w = 45
    header = f"{'Pipe':<{pipe_w}}" + "".join(f"{l:^{col_w}}" for l in snap_labels)
    print(header)
    print("-" * len(header))

    # Status markers
    markers = {
        "functional": "✓",
        "broken": "✗",
        "stressed": "~",
        "repaired": "↑",
        "unknown": "?",
    }

    for pipe in pipes:
        indent = "  " * pipe["depth"]
        label = pipe["description"][:pipe_w - len(indent) - 5]
        stack_tag = f"[{pipe['stack'][0]}]" if pipe["stack"] else "   "
        row = f"{indent}{stack_tag} {label:<{pipe_w - len(indent) - 4}}"

        for snap in snapshots:
            state = db.execute(
                "SELECT status FROM pipe_state WHERE pipe_id = ? AND snapshot_id = ?",
                (pipe["id"], snap["id"]),
            ).fetchone()
            marker = markers.get(state["status"], " ") if state else " "
            row += f"{marker:^{col_w}}"

        print(row)

    db.close()


def show_trajectory(company_id):
    """Show state transitions for each pipe across snapshots."""
    db = _db()

    snapshots = db.execute(
        "SELECT id, label FROM snapshot WHERE company_id = ? ORDER BY date_start",
        (company_id,),
    ).fetchall()

    pipes = db.execute(
        "SELECT id, description, stack, site FROM pipe WHERE company_id = ? ORDER BY depth, id",
        (company_id,),
    ).fetchall()

    for pipe in pipes:
        states = []
        for snap in snapshots:
            state = db.execute(
                "SELECT status, evidence FROM pipe_state WHERE pipe_id = ? AND snapshot_id = ?",
                (pipe["id"], snap["id"]),
            ).fetchone()
            if state:
                states.append((snap["label"], state["status"], state["evidence"]))

        if not states:
            continue

        # Check for transitions
        transitions = []
        for i in range(1, len(states)):
            if states[i][1] != states[i - 1][1]:
                transitions.append(f"{states[i-1][0]}({states[i-1][1]}) → {states[i][0]}({states[i][1]})")

        if transitions:
            tag = f"[{pipe['stack'][0]}]" if pipe["stack"] else "   "
            print(f"{tag} {pipe['description']}")
            for t in transitions:
                print(f"    {t}")
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
        print("Usage: diagnose.py [temporal TICKER | trajectory TICKER | scorecard]")
        sys.exit(1)

    cmd = sys.argv[1]
    db = _db()

    if cmd in ("temporal", "trajectory") and len(sys.argv) >= 3:
        row = db.execute("SELECT id FROM company WHERE ticker = ?", (sys.argv[2].upper(),)).fetchone()
        db.close()
        if not row:
            print(f"Company {sys.argv[2]} not found.")
            sys.exit(1)
        if cmd == "temporal":
            show_temporal(row["id"])
        else:
            show_trajectory(row["id"])
    elif cmd == "scorecard":
        db.close()
        show_scorecard()
    else:
        db.close()
        print("Usage: diagnose.py [temporal TICKER | trajectory TICKER | scorecard]")
