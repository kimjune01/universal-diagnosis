"""Initialize the database and seed with Shkreli's biotech targets."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "diagnosis.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def init():
    # Delete existing DB to start fresh with temporal schema
    if DB_PATH.exists():
        DB_PATH.unlink()

    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA_PATH.read_text())

    # Seed companies from Shkreli's 2025-2026 positions
    companies = [
        ("CAPR", "Capricor Therapeutics", "biotech",
         "Shkreli shorted, said HOPE-3 'will not work'. Stock +440% on positive Phase 3. Admitted 'bad call'. Run 0 demonstration."),
        ("SPRB", "Spruce Biosciences", "biotech",
         "Shkreli long, targets $500, says TA-ERT 'will be approved'. BLA submission expected Q4 2026. Run 1 forward."),
        ("QURE", "uniQure", "biotech",
         "Shkreli was long on AMT-130 (Huntington's gene therapy), saw 5-10x, sold Nov 2025. Run 0 demonstration."),
        ("ATYR", "aTyr Pharma", "biotech",
         "Shkreli short, predicted 80% crash. FDA Type C meeting mid-April 2026. Run 1 forward."),
        ("INMB", "Inmune Bio", "biotech",
         "Shkreli predicted 90% drop. MAA submission mid-summer 2026. Run 1 forward."),
    ]

    for ticker, name, sector, notes in companies:
        db.execute(
            "INSERT OR IGNORE INTO company (ticker, name, sector, notes) VALUES (?, ?, ?, ?)",
            (ticker, name, sector, notes),
        )

    # Seed CAPR pipe topology (stable across time)
    capr_id = db.execute("SELECT id FROM company WHERE ticker = 'CAPR'").fetchone()[0]

    # Root pipe
    root = _add_pipe(db, capr_id, "Deramiocel (CAP-1002) for DMD", None, None, None)

    # Cache stack (forward pass)
    p2c = _add_pipe(db, capr_id, "Compound enters biological system", "cache", "perceive_cache", root)
    c2f = _add_pipe(db, capr_id, "Therapeutic vs adverse effect separation", "cache", "cache_filter", root)
    f2a = _add_pipe(db, capr_id, "Endpoint selection and therapeutic window", "cache", "filter_attend", root)
    a2r = _add_pipe(db, capr_id, "Durability and regulatory path", "cache", "attend_remember", root)

    # Consolidate stack (backward pass = the company)
    read = _add_pipe(db, capr_id, "Clinical data collection and interpretation", "consolidate", "read_outcomes", root)
    batch = _add_pipe(db, capr_id, "Strategic decisions between trials", "consolidate", "batch_process", root)
    write = _add_pipe(db, capr_id, "Changes to molecule, manufacturing, trial design", "consolidate", "write_substrate", root)

    # Seed snapshots for CAPR (4 temporal snapshots from smoke test findings)
    snapshots = [
        ("ALLSTAR era", "2012-01-01", "2017-06-30"),
        ("HOPE-1 era", "2016-01-01", "2019-12-31"),
        ("HOPE-2 / BLA era", "2018-01-01", "2025-07-11"),
        ("HOPE-3 era", "2022-01-01", "2025-12-31"),
    ]

    for label, start, end in snapshots:
        db.execute(
            "INSERT INTO snapshot (company_id, label, date_start, date_end) VALUES (?, ?, ?, ?)",
            (capr_id, label, start, end),
        )

    # Seed known traumas for CAPR
    traumas = [
        (capr_id, None, "ALLSTAR Phase I/II failed primary endpoint (scar reduction in MI), stopped for futility",
         "2017-01-01", "https://pubmed.ncbi.nlm.nih.gov/32749459/", "indication_mechanism_failure"),
        (capr_id, f2a, "FDA CRL: BLA based on HOPE-2 (n=20) 'did not meet substantial evidence of effectiveness'",
         "2025-07-11", "https://www.sec.gov/Archives/edgar/data/1133869/000155837025009186/capr-20250711x8k.htm", "regulatory_evidence_packaging"),
        (capr_id, None, "Shkreli publishes 46-page short report, stock drops 17%",
         "2025-11-24", "https://x.com/MartinShkreli/status/1992971976294498581", "analyst_short_attack"),
        (capr_id, None, "HOPE-3 Phase 3 positive topline: PUL v2.0 p=0.029, LVEF p=0.041, stock +440%",
         "2025-12-03", "https://www.benzinga.com/markets/biotech/25/12/49251640", "trial_success"),
    ]

    for company_id, pipe_id, desc, date, url, cat in traumas:
        db.execute(
            "INSERT INTO trauma (company_id, pipe_id, description, date, source_url, category) VALUES (?, ?, ?, ?, ?, ?)",
            (company_id, pipe_id, desc, date, url, cat),
        )

    db.commit()
    print(f"Database initialized at {DB_PATH}")
    print(f"  {db.execute('SELECT count(*) FROM company').fetchone()[0]} companies")
    print(f"  {db.execute('SELECT count(*) FROM pipe').fetchone()[0]} pipes")
    print(f"  {db.execute('SELECT count(*) FROM snapshot').fetchone()[0]} snapshots")
    print(f"  {db.execute('SELECT count(*) FROM trauma').fetchone()[0]} traumas")
    db.close()


def _add_pipe(db, company_id, description, stack, site, parent_id):
    depth = 0
    if parent_id is not None:
        row = db.execute("SELECT depth FROM pipe WHERE id = ?", (parent_id,)).fetchone()
        if row:
            depth = row[0] + 1
    cur = db.execute(
        "INSERT INTO pipe (company_id, parent_id, description, stack, site, depth) VALUES (?, ?, ?, ?, ?, ?)",
        (company_id, parent_id, description, stack, site, depth),
    )
    return cur.lastrowid


if __name__ == "__main__":
    init()
