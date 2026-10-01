-- =============================================================================
-- ESQUEMA DO BANCO DE DADOS (POSTGRESQL)
-- Sistema de Agente de IA para WhatsApp & Agendamento Automático (Bacci Dev)
-- =============================================================================

-- 1. Tabela de Estabelecimentos (Multi-Tenant)
CREATE TABLE IF NOT EXISTS public.estabelecimentos (
    id SERIAL PRIMARY KEY,
    instancia VARCHAR(100) UNIQUE NOT NULL,
    nome_agente VARCHAR(100) NOT NULL,
    nome_estabelecimento VARCHAR(200) NOT NULL,
    tipo_estabelecimento VARCHAR(100),
    nome_profissional VARCHAR(200),
    especialidade VARCHAR(200),
    endereco TEXT,
    telefone_atendente VARCHAR(50),
    forma_pagamento TEXT,
    horario_funcionamento TEXT,
    observacoes_adicionais TEXT,
    google_calendar_id VARCHAR(255),
    google_access_token TEXT,
    google_refresh_token TEXT,
    server_url VARCHAR(255),
    apikey VARCHAR(255),
    ativo BOOLEAN DEFAULT TRUE,
    lembrete_ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Tabela de Catálogo de Serviços e Procedimentos
CREATE TABLE IF NOT EXISTS public.servicos (
    id SERIAL PRIMARY KEY,
    instancia VARCHAR(100) NOT NULL,
    nome VARCHAR(200) NOT NULL,
    categoria VARCHAR(100),
    descricao TEXT,
    duracao_minutos INTEGER DEFAULT 30,
    tipo_precificacao VARCHAR(50) DEFAULT 'fixo',
    valor_fixo NUMERIC(10, 2),
    valor_base NUMERIC(10, 2),
    observacao_valor TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_servicos_instancia FOREIGN KEY (instancia) REFERENCES public.estabelecimentos(instancia) ON DELETE CASCADE
);

-- 3. Tabela de Leads e Controle de Atendimento Humano
CREATE TABLE IF NOT EXISTS public.leads (
    id SERIAL PRIMARY KEY,
    instance_name VARCHAR(100) NOT NULL,
    nome VARCHAR(200),
    numero VARCHAR(50) NOT NULL,
    atendimento_humano BOOLEAN DEFAULT FALSE,
    atendimento_pausado_em TIMESTAMP WITH TIME ZONE,
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT uq_leads_instancia_numero UNIQUE (instance_name, numero)
);

-- 4. Tabela de Lembretes Enviados (Evita envios duplicados)
CREATE TABLE IF NOT EXISTS public.lembretes_enviados (
    google_event_id VARCHAR(255) PRIMARY KEY,
    enviado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Tabela de Histórico de Conversas da IA (Memória n8n)
CREATE TABLE IF NOT EXISTS public.n8n_chat_histories (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    message JSONB NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_histories_session ON public.n8n_chat_histories(session_id);
