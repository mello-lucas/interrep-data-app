
# 🏗️ Interrep — Data App  

**Data product para análise de campeonatos esportivos, construído com arquitetura moderna de dados (RAW → SILVER → GOLD), dbt e Streamlit.**

---

## 📌 Overview

Interrep é um sistema analítico que transforma planilhas de resultados em métricas consolidadas e dashboards interativos.

O projeto foi desenvolvido com foco em:

- Arquitetura profissional de dados  
- Modelagem dimensional (Star Schema)  
- Separação clara entre ingestão, transformação e consumo  
- Performance e governança  
- Reprodutibilidade e idempotência  

O usuário interage apenas com:

- Upload de planilha  
- Dashboard analítico  

Toda a engenharia de dados ocorre nos bastidores.

---

# 🧱 Arquitetura

```
Excel Upload
     ↓
RAW (append-only)
     ↓
SILVER (Star Schema)
     ↓
GOLD (tabelas analíticas)
     ↓
Streamlit Dashboard
```

## 🔹 Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| Banco | PostgreSQL (Neon - serverless) |
| Transformação | dbt Core |
| Ingestão | Python (pandas) |
| Frontend | Streamlit |
| Orquestração | GitHub Actions |

---

# 🗂 Estrutura de Camadas

## 1️⃣ RAW

- Espelhamento 1:1 da planilha
- Estrutura append-only
- Controle por `ingestion_at`
- Nenhuma regra de negócio aplicada

Objetivo: preservação fiel dos dados brutos.

---

## 2️⃣ SILVER

Modelagem dimensional com dbt.

### Dimensões
- `dim_player`
- `dim_game`
- `dim_championship`
- `dim_round`

### Fato
- `fact_player_game_stats`
  - Grain: 1 jogador × 1 jogo

Inclui:
- Deduplicação
- Padronização
- Testes (`not_null`, `unique`, `relationships`)

Objetivo: consistência e reutilização analítica.

---

## 3️⃣ GOLD

Tabelas otimizadas para consumo no dashboard.

Exemplos:
- `gold_match_scoreboard`
- `gold_player_season_stats`
- `gold_team_leaderboards`
- `gold_championship_kpis`

Características:
- Métricas consolidadas
- Agregações pré-computadas
- Sem lógica pesada no front-end
- Única camada consumida pelo Streamlit

---

# ⚙️ Pipeline de Dados

## Ingestão

1. Admin realiza upload da planilha
2. Validação estrutural
3. Inserção append-only na RAW

## Transformação

Executado via dbt:

```
RAW → SILVER → GOLD
```

- Construção do Star Schema
- Regras de negócio consolidadas
- Agregações finais

## Orquestração

- GitHub Actions
- Execução automatizada
- Reprocessamento idempotente

---

# 📊 Dashboard

O aplicativo Streamlit:

- Conecta apenas ao schema `gold`
- Utiliza cache (`st.cache_data`)
- Executa queries consolidadas
- Permite filtros por:
  - Ano
  - Campeonato
  - Time

### Funcionalidades atuais

- KPIs consolidados
- Rankings de jogadores
- Estatísticas por jogo
- Destaque automático para artilheiro
- Métricas como:
  - % jogos com gol
  - Blue cards

---

# 🔐 Governança

- Separação de usuários no banco:
  - `ingestion_user` → INSERT em RAW
  - `analytics_user` → SELECT em GOLD
- Ingestão protegida (admin-only)
- Arquitetura orientada a controle e auditabilidade

---

# 🎯 Objetivo do Projeto

Demonstrar na prática:

- Arquitetura moderna de dados  
- Analytics Engineering com dbt  
- Modelagem dimensional real  
- Construção de data products  
- Boas práticas de performance e governança  

O projeto evolui de dashboard esportivo para um **case completo de engenharia e produto analítico**.

---

# 🚀 Próximos Passos

- Métrica de Impacto Ofensivo  
- Goal Share (participação nos gols do time)  
- Comparação entre times  
- Aba Campeonato (visão macro)  
- Aba Jogadores (análise longitudinal)  
- CRUD controlado para entidade Games  

---

# 📌 Resumo

Interrep é um projeto orientado a arquitetura.

O usuário vê:

- Planilhas  
- Rankings  
- KPIs  

A engenharia por trás envolve:

- Modelagem dimensional  
- dbt  
- Arquitetura em camadas  
- Serverless  
- Orquestração automatizada  
- Governança de dados  
