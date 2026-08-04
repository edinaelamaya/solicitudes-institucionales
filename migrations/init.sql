CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    external_identifier VARCHAR(100) NOT NULL,
    category VARCHAR(60) NOT NULL,
    requester_name VARCHAR(150) NOT NULL,
    requester_email VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'recibida',
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT uq_requests_external_identifier UNIQUE (external_identifier)
);

CREATE INDEX IF NOT EXISTS ix_requests_status ON requests (status);
CREATE INDEX IF NOT EXISTS ix_requests_category ON requests (category);
CREATE INDEX IF NOT EXISTS ix_requests_priority ON requests (priority);
CREATE INDEX IF NOT EXISTS ix_requests_external_identifier ON requests (external_identifier);
