# 🤖 Sistema de Agente de IA para WhatsApp & Agendamento Inteligente (n8n)
> **Solução completa e modular de atendimento conversacional 24/7 com IA, sincronização em tempo real com Google Agenda e disparo automático de lembretes 2 horas antes da consulta.**  
> *Desenvolvido por **Bacci Dev** (Iago Bacci)*

---

![n8n](https://img.shields.io/badge/n8n-Modular%20Workflows-FF6584?style=for-the-badge&logo=n8n)
![WhatsApp](https://img.shields.io/badge/WhatsApp-Evolution%20API-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)
![Google Calendar](https://img.shields.io/badge/Google%20Calendar-Sync%20API-4285F4?style=for-the-badge&logo=googlecalendar&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🎯 Sobre o Projeto

Este projeto é um ecossistema completo de **agente de inteligência artificial para WhatsApp** com integração nativa ao **Google Agenda** e banco de dados **PostgreSQL**.

Diferente de chatbots básicos engessados, o sistema opera de forma **100% dinâmica e modular**, suportando múltiplos estabelecimentos (multi-tenant) e utilizando IA para entender linguagem natural, tirar dúvidas sobre serviços e preços, verificar disponibilidade na agenda, criar, atualizar e cancelar agendamentos, além de enviar lembretes automáticos para reduzir o índice de faltas (*no-show*).

---

## 🏗️ Arquitetura dos 8 Workflows

O sistema é dividido em **1 Agente Orquestrador**, **5 Ferramentas (Sub-workflows)** e **2 Rotinas em Segundo Plano**:

```mermaid
flowchart TD
    Lead["👤 Cliente no WhatsApp"] <-->|Mensagem / Áudio| Evo["📲 Evolution API"]
    Evo <-->|Webhook em Tempo Real| Bot["🧠 1. BOT Agendamento Dinâmico (Core)"]
    
    subgraph Ferramentas do Agente (AI Tools)
        Bot -->|Tool| T1["📅 2. Criar Agendamento"]
        Bot -->|Tool| T2["🔍 3. Verificar Disponibilidade"]
        Bot -->|Tool| T3["🔎 4. Buscar Eventos Existentes"]
        Bot -->|Tool| T4["🔄 5. Atualizar Agendamento"]
        Bot -->|Tool| T5["❌ 6. Cancelar Agendamento"]
    end
    
    T1 & T2 & T3 & T4 & T5 <-->|Leitura e Gravação| GCal["📆 Google Calendar API"]
    Bot <-->|Memória e Regras de Negócio| DB[("🗄️ PostgreSQL Database")]
    
    subgraph Rotinas Automáticas (Background)
        Cron1["⏰ Schedule Diário"] --> R1["📦 7. Arquivar Agendamentos Passados"]
        Cron2["⏰ Schedule a cada minuto"] --> R2["🔔 8. Lembretes Automáticos (2h Antes)"]
    end
    
    R1 --> DB
    R2 -->|Busca eventos em 2h| GCal
    R2 -->|Dispara Lembrete via WhatsApp| Evo
```

---

## 📁 Estrutura do Repositório

```text
├── workflows/
│   ├── 1_BOT_Agendamento_Dinamico_v2.json           # Agente Principal (Orquestração, IA e Memória)
│   ├── 2_Criar_Agendamento_Dinamico_v2.json         # Tool: Criação de consulta no Google Calendar
│   ├── 3_Verificar_Disponibilidade_Dinamico_v2.json # Tool: Consulta de slots livres sem conflito
│   ├── 4_Buscar_Eventos_Existentes.json             # Tool: Localização de agendamentos do cliente
│   ├── 5_Atualizar_Agendamento_Tool.json            # Tool: Remarcação de data e horário
│   ├── 6_Cancelar_Agendamento_Tool.json             # Tool: Cancelamento e liberação do horário
│   ├── 7_Arquivar_Agendamentos_Passados.json        # Rotina: Arquivamento de histórico passado
│   └── 8_Lembretes_Automaticos_Workflow.json        # Rotina: Lembrete automático 2h antes no WhatsApp
├── database/
│   └── schema.sql                                  # DDL completo das tabelas PostgreSQL
├── docs/
│   └── midia_kit_bacci_dev.md                      # Mídia Kit comercial da solução
├── .env.example                                    # Modelo de variáveis de ambiente
├── .gitignore                                      # Proteção de credenciais e dados locais
└── README.md                                       # Documentação completa
```

---

## ⚡ Principais Funcionalidades

1. **Atendimento Humanizado 24/7:** O agente compreende variações linguísticas, gírias e solicitações contextuais, respondendo com naturalidade.
2. **Consulta e Agendamento em Tempo Real:** Conecta-se diretamente à API do Google Calendar para checar conflitos antes de confirmar.
3. **Gestão Completa do Agendamento:** Permite remarcar ou cancelar consultas diretamente pelo chat do WhatsApp.
4. **Lembrete Automático 2 Horas Antes:** Um cron verifica a agenda a cada minuto e envia automaticamente uma mensagem personalizada de confirmação com opções de resposta, salvando no banco para nunca enviar duplicado.
5. **Transbordo para Atendimento Humano:** Caso o cliente solicite falar com um atendente, o bot pausa a automação para aquele número por 4 horas automaticamente.
6. **Multi-Tenant (Múltiplas Empresas):** O banco de dados suporta instâncias isoladas com agentes, nomes de profissionais, especialidades e calendários próprios.

---

## 🛠️ Como Instalar e Configurar

### 1. Banco de Dados (PostgreSQL)
1. Conecte-se à sua instância PostgreSQL (Docker, VPS ou servidor de banco de dados).
2. Abra seu gerenciador de banco (DBeaver, pgAdmin, psql ou interface web).
3. Execute o script contido em [`database/schema.sql`](database/schema.sql).
4. As tabelas `estabelecimentos`, `servicos`, `leads`, `lembretes_enviados` e `n8n_chat_histories` serão criadas com todos os índices necessários.

### 2. Configurar o n8n
1. No seu painel do n8n, crie uma pasta para o projeto.
2. Importe os **8 arquivos** da pasta `workflows/` na seguinte ordem de referência:
   - Primeiro os sub-workflows (arquivos `2_` a `6_`).
   - Em seguida as rotinas em segundo plano (arquivos `7_` e `8_`).
   - Por fim, o agente principal (`1_BOT_Agendamento_Dinamico_v2.json`).
3. Conecte suas credenciais do **PostgreSQL** e **Evolution API** nos nós correspondentes.
4. Configure as variáveis de ambiente baseadas no arquivo `.env.example`.

### 3. Conectar a Evolution API
- Aponte o Webhook da sua instância na Evolution API para a URL do Webhook do workflow `1_BOT_Agendamento_Dinamico_v2`.
- Eventos recomendados: `MESSAGES_UPSERT`.

---

## 🛡️ Segurança & Boas Práticas

- **Credenciais Sanitizadas:** Todos os arquivos de workflow deste repositório tiveram seus identificadores reais, Client Secrets e tokens OAuth substituídos por placeholders seguros.
- **Isolamento de Memória:** O histórico de conversa é indexado por chave de sessão com expiração e controle de transbordo humano.

---

## 👨‍💻 Autor & Contato

**Iago Bacci** (Bacci Dev)  
*Especialista em Desenvolvimento Web, Inteligência Artificial e Automação de Processos.*

- **Instagram:** [@baccidev](https://instagram.com/baccidev)
- **WhatsApp:** [Fale comigo no WhatsApp](https://wa.me/5511917163127)
- **GitHub:** [github.com/iagobacci](https://github.com/iagobacci)

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
