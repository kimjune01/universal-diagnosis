"""Initialize the database and seed with Shkreli's biotech targets."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "diagnosis.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def init():
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA_PATH.read_text())

    # Seed companies from Shkreli's 2025-2026 positions
    companies = [
        ("CAPR", "Capricor Therapeutics", "biotech",
         "Shkreli shorted, said HOPE-3 'will not work'. Stock +440% on positive Phase 3. Admitted 'bad call'. Retrospective target."),
        ("SPRB", "Spruce Biosciences", "biotech",
         "Shkreli long, targets $500, says TA-ERT 'will be approved'. BLA submission expected Q4 2026. Forward target."),
        ("QURE", "uniQure", "biotech",
         "Shkreli was long on AMT-130 (Huntington's gene therapy), saw 5-10x, sold Nov 2025."),
        ("ATYR", "aTyr Pharma", "biotech",
         "Shkreli short, predicted 80% crash within six weeks."),
        ("INMB", "Inmune Bio", "biotech",
         "Shkreli predicted 90% drop."),
    ]

    for ticker, name, sector, notes in companies:
        db.execute(
            "INSERT OR IGNORE INTO company (ticker, name, sector, notes) VALUES (?, ?, ?, ?)",
            (ticker, name, sector, notes),
        )

    # Seed known traumas for CAPR (retrospective case)
    capr_id = db.execute("SELECT id FROM company WHERE ticker = 'CAPR'").fetchone()[0]

    traumas = [
        (capr_id, "Shkreli publishes 46-page short report, stock drops 17%",
         "2025-11-01", "https://x.com/MartinShkreli/status/1992971976294498581",
         "analyst_short_attack"),
        (capr_id, "HOPE-3 Phase 3 positive results, stock +440%",
         "2025-12-01", "https://www.benzinga.com/markets/biotech/25/12/49251640",
         "trial_success"),
    ]

    for company_id, desc, date, url, cat in traumas:
        db.execute(
            "INSERT OR IGNORE INTO trauma (company_id, description, date, source_url, category) VALUES (?, ?, ?, ?, ?)",
            (company_id, desc, date, url, cat),
        )

    db.commit()
    print(f"Database initialized at {DB_PATH}")
    print(f"  {db.execute('SELECT count(*) FROM company').fetchone()[0]} companies")
    print(f"  {db.execute('SELECT count(*) FROM trauma').fetchone()[0]} traumas")
    db.close()


if __name__ == "__main__":
    init()
