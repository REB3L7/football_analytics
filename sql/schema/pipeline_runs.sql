CREATE TABLE IF NOT EXISTS live.pipeline_runs (
    run_id BIGSERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'running',
    matches_discovered INTEGER DEFAULT 0,
    matches_processed INTEGER DEFAULT 0,
    matches_failed INTEGER DEFAULT 0,
    player_records_processed INTEGER DEFAULT 0,
    error_message TEXT,
    CONSTRAINT valid_pipeline_status
    CHECK (
        status IN (
            'running',
            'success',
            'failed',
            'partial_success',
            'rate_limited'
    )
)
);
