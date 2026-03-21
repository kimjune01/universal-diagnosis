-- Universal Diagnosis: SQLite schema
-- Recursive pipe tree + predictions + scorecard

-- A company being diagnosed
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY,
    ticker TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    sector TEXT NOT NULL DEFAULT 'biotech',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- A pipe node in the recursive tree (topology — stable across time)
-- Every node is a pipe. Every pipe has the same shape.
CREATE TABLE IF NOT EXISTS pipe (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    parent_id INTEGER REFERENCES pipe(id),
    description TEXT NOT NULL,          -- marketing-speak name
    stack TEXT CHECK(stack IN ('cache', 'consolidate')),
    site TEXT,                          -- handoff or stage within the stack
    depth INTEGER NOT NULL DEFAULT 0,
    is_rock_bottom INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(company_id, stack, site)      -- one pipe per role per company
);

-- An event: a public record that changes a pipe's state.
-- The temporal graph grows one event at a time.
-- Peters' sequence-based dynamic graph: G_i = (V, E_i) at time i,
-- where i is the archival date of the record.
CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY,
    pipe_id INTEGER NOT NULL REFERENCES pipe(id),
    source_date TEXT NOT NULL,          -- archival date of the public record
    status TEXT NOT NULL
        CHECK(status IN ('functional', 'broken', 'stressed', 'repaired', 'unknown')),
    evidence TEXT NOT NULL,             -- what the record says
    source_url TEXT NOT NULL,           -- link to the public record
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Embedding for pipe descriptions (deduplication + semantic search)
CREATE TABLE IF NOT EXISTS pipe_embedding (
    pipe_id INTEGER PRIMARY KEY REFERENCES pipe(id),
    embedding BLOB NOT NULL,            -- float32 vector, serialized
    model TEXT NOT NULL DEFAULT 'all-MiniLM-L6-v2'
);

-- Known failures for recurrence probes
CREATE TABLE IF NOT EXISTS trauma (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    pipe_id INTEGER REFERENCES pipe(id),
    description TEXT NOT NULL,
    date TEXT,                          -- when it happened
    source_url TEXT,                    -- link to public evidence
    category TEXT,                      -- failure class for recurrence matching
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Embedding for trauma descriptions (similarity matching)
CREATE TABLE IF NOT EXISTS trauma_embedding (
    trauma_id INTEGER PRIMARY KEY REFERENCES trauma(id),
    embedding BLOB NOT NULL,
    model TEXT NOT NULL DEFAULT 'all-MiniLM-L6-v2'
);

-- A prediction generated from diagnosis
-- The prediction is the falsifiable artifact. SOAP notes are disposable reasoning.
-- Three arms per company-catalyst: temporal, snapshot, analyst.
CREATE TABLE IF NOT EXISTS prediction (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    pipe_id INTEGER REFERENCES pipe(id),
    arm TEXT NOT NULL DEFAULT 'temporal'
        CHECK(arm IN ('temporal', 'snapshot', 'analyst')),
    type TEXT
        CHECK(type IN ('recurrence', 'cascade', 'fix', 'death', 'mitosis')),
    category TEXT
        CHECK(category IN ('living_well', 'living_dying', 'dying_pivoted', 'dying_dying')),
    direction TEXT NOT NULL             -- the binary call
        CHECK(direction IN ('pass', 'fail')),
    catalyst TEXT NOT NULL,             -- exact event, e.g., "HOPE-3 Phase 3 topline readout"
    resolution_source TEXT NOT NULL,    -- exact source that determines outcome
    window_start TEXT NOT NULL,         -- scoring window opens
    window_end TEXT NOT NULL,           -- scoring window closes
    pass_condition TEXT NOT NULL,       -- exact condition for PASS
    reasoning TEXT NOT NULL,            -- one sentence — temporal trajectory, not snapshot
    run TEXT NOT NULL                   -- 'run0' or 'run1'
        CHECK(run IN ('run0', 'run1')),
    published_at TEXT,                  -- when we published (timestamp = priority)
    outcome TEXT CHECK(outcome IN ('hit', 'miss', 'void', 'pending'))
        DEFAULT 'pending',
    outcome_notes TEXT,
    outcome_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Financial snapshots for runway calculation
CREATE TABLE IF NOT EXISTS financial_snapshot (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    cash INTEGER NOT NULL,
    quarterly_burn INTEGER NOT NULL,
    source_date TEXT NOT NULL,
    source_url TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Scorecard: all published predictions, three arms per company-catalyst
CREATE VIEW IF NOT EXISTS scorecard AS
SELECT
    p.id AS prediction_id,
    c.ticker,
    c.name AS company_name,
    p.arm,
    p.type,
    p.category,
    p.direction,
    p.catalyst,
    p.window_end,
    p.pass_condition,
    p.reasoning,
    p.run,
    p.published_at,
    p.outcome
FROM prediction p
JOIN company c ON c.id = p.company_id
WHERE p.published_at IS NOT NULL
ORDER BY p.catalyst, c.ticker, p.arm;
