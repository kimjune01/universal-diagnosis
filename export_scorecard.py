"""Export the scorecard from SQLite to scorecard.json for the dashboard."""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "diagnosis.db"
OUT_PATH = Path(__file__).parent / "scorecard.json"


def export():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row

    rows = db.execute("""
        SELECT
            c.ticker,
            p.run,
            p.arm,
            p.category,
            p.direction,
            p.catalyst,
            p.window_end,
            p.outcome
        FROM prediction p
        JOIN company c ON c.id = p.company_id
        WHERE p.published_at IS NOT NULL
        ORDER BY p.catalyst, c.ticker, p.arm
    """).fetchall()

    predictions = [dict(r) for r in rows]

    data = {"predictions": predictions}
    OUT_PATH.write_text(json.dumps(data, indent=2))

    hits = sum(1 for p in predictions if p["outcome"] == "hit")
    misses = sum(1 for p in predictions if p["outcome"] == "miss")
    pending = sum(1 for p in predictions if p["outcome"] == "pending")

    print(f"Exported {len(predictions)} predictions to {OUT_PATH}")
    print(f"  {hits} hits, {misses} misses, {pending} pending")

    db.close()


if __name__ == "__main__":
    export()
