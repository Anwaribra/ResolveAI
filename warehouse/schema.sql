-- ResolveAI PostgreSQL Schema Initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    tier VARCHAR(50) DEFAULT 'standard' CHECK (tier IN ('standard', 'premium', 'enterprise')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Products Table
CREATE TABLE IF NOT EXISTS products (
    product_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tickets Table
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES customers(customer_id) ON DELETE SET NULL,
    product_id UUID REFERENCES products(product_id) ON DELETE SET NULL,
    subject VARCHAR(500) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'NEW' CHECK (
        status IN (
            'NEW', 'CLASSIFIED', 'RETRIEVED', 'RESPONSE_GENERATED',
            'DECISION_PENDING', 'AUTO_RESOLVED', 'ESCALATED', 'HUMAN_RESOLVED'
        )
    ),
    priority VARCHAR(50) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Ticket Messages Table
CREATE TABLE IF NOT EXISTS ticket_messages (
    message_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    sender_type VARCHAR(50) NOT NULL CHECK (sender_type IN ('customer', 'agent', 'ai')),
    body TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Ticket Events Audit Log Table
CREATE TABLE IF NOT EXISTS ticket_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. AI Predictions Table
CREATE TABLE IF NOT EXISTS ai_predictions (
    prediction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    predicted_category VARCHAR(100) NOT NULL,
    predicted_intent VARCHAR(100) NOT NULL,
    predicted_priority VARCHAR(50) NOT NULL,
    confidence_score NUMERIC(5, 4) NOT NULL,
    retrieval_quality NUMERIC(5, 4) NOT NULL,
    generated_response TEXT NOT NULL,
    retrieved_chunk_ids JSONB DEFAULT '[]'::jsonb,
    decision VARCHAR(50) NOT NULL CHECK (decision IN ('AUTO_RESOLVE', 'ESCALATE')),
    model_version VARCHAR(100) NOT NULL,
    prompt_version VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Resolutions Table
CREATE TABLE IF NOT EXISTS resolutions (
    resolution_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    resolved_by VARCHAR(50) NOT NULL CHECK (resolved_by IN ('ai', 'human_agent')),
    final_category VARCHAR(100),
    satisfaction_score INTEGER CHECK (satisfaction_score BETWEEN 1 AND 5),
    resolved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Escalations Table
CREATE TABLE IF NOT EXISTS escalations (
    escalation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_id UUID NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    reason VARCHAR(255) NOT NULL,
    assigned_agent_id UUID,
    escalated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Knowledge Documents Table
CREATE TABLE IF NOT EXISTS knowledge_documents (
    document_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 10. Knowledge Chunks Table (Vector Store)
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    chunk_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES knowledge_documents(document_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(768),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_customer ON tickets(customer_id);
CREATE INDEX IF NOT EXISTS idx_ticket_events_ticket ON ticket_events(ticket_id);
CREATE INDEX IF NOT EXISTS idx_ai_predictions_ticket ON ai_predictions(ticket_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_vector ON knowledge_chunks USING hnsw (embedding vector_cosine_ops);
