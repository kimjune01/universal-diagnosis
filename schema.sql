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

-- A pipe node in the recursive tree
-- Every node is a pipe. Every pipe has the same shape.
CREATE TABLE IF NOT EXISTS pipe (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    parent_id INTEGER REFERENCES pipe(id),
    description TEXT NOT NULL,          -- marketing-speak name
    stack TEXT CHECK(stack IN ('cache', 'consolidate')),
    site TEXT,                          -- handoff or stage within the stack
    depth INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'unexplored'
        CHECK(status IN ('unexplored', 'claimed', 'diagnosed', 'cleared')),
    diagnosis TEXT,                     -- conclusion, if any
    is_rock_bottom INTEGER NOT NULL DEFAULT 0,
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
CREATE TABLE IF NOT EXISTS prediction (
    id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    pipe_id INTEGER REFERENCES pipe(id),
    type TEXT NOT NULL
        CHECK(type IN ('recurrence', 'cascade', 'fix', 'death', 'mitosis')),
    claim TEXT NOT NULL,                -- the falsifiable statement
    evidence TEXT,                      -- what supports the diagnosis
    catalyst_date TEXT,                 -- when outcome will be known
    timeframe TEXT,                     -- how long the prediction window is
    published_at TEXT,                  -- when we published (timestamp = priority)
    outcome TEXT CHECK(outcome IN ('confirmed', 'refuted', 'void', 'pending')),
    outcome_notes TEXT,
    outcome_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Analyst positions for head-to-head comparison
CREATE TABLE IF NOT EXISTS analyst_call (
    id INTEGER PRIMARY KEY,
    prediction_id INTEGER NOT NULL REFERENCES prediction(id),
    analyst_name TEXT NOT NULL,
    position TEXT NOT NULL,             -- what they predicted
    source_url TEXT,
    call_date TEXT,
    outcome TEXT CHECK(outcome IN ('correct', 'incorrect', 'void', 'pending')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Scorecard view
CREATE VIEW IF NOT EXISTS scorecard AS
SELECT
    p.id AS prediction_id,
    c.ticker,
    c.name AS company_name,
    p.type,
    p.claim,
    p.catalyst_date,
    p.outcome AS framework_outcome,
    a.analyst_name,
    a.position AS analyst_position,
    a.outcome AS analyst_outcome
FROM prediction p
JOIN company c ON c.id = p.company_id
LEFT JOIN analyst_call a ON a.prediction_id = p.id
ORDER BY p.catalyst_date;
