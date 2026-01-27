# 🏗️ Interrep — Data App  
## Roadmap Técnico & Experiência do Usuário Final

Este documento apresenta **duas visões complementares** do projeto:

1. **Plano de Execução (Tasks Técnicas)** — o que precisa ser construído, em ordem lógica  
2. **Fluxo do Produto Final (Visão do Cliente)** — como o sistema funciona do ponto de vista do usuário

O objetivo é deixar explícito **o que será feito**, **por quê** e **como cada parte se conecta**, seguindo boas práticas de Analytics Engineering.

---

# 1️⃣ Plano de Execução — Tasks Técnicas

## 1. Planejamento e Fonte de Dados
- Definir layout final da planilha (schema estável)
  - Identificadores únicos: jogador, jogo, campeonato, rodada
  - Tipagem clara (int, float, date, text)
- Definir regras de negócio explícitas:
  - O que é um jogo válido
  - Como lidar com jogadores ausentes
  - Métricas primárias (gols, assistências, cartões)

---

## 2. Camada RAW — Ingestão
**Objetivo:** persistir os dados exatamente como recebidos (sem lógica de negócio)

### Estrutura
- `raw.mirror_base`
  - Espelha 1:1 a planilha
  - Append-only (nunca atualiza ou deleta)

### Implementação
- Script Python de ingestão:
  - Leitura do Excel (`pandas`)
  - Validação mínima de schema
  - Insert direto no PostgreSQL (Neon)
- Alternativa (mais produto):
  - Painel admin no Streamlit
  - Upload do Excel
  - Controle de permissões (admin-only)

---

## 3. Infraestrutura de Banco (Neon)
- PostgreSQL serverless
- Schemas separados:
  - `raw`
  - `silver`
  - `gold`
- Usuários distintos:
  - `ingestion_user` → INSERT apenas em RAW
  - `analytics_user` → SELECT em GOLD

---

## 4. Camada SILVER — Modelagem Dimensional
**Objetivo:** criar um Star Schema limpo, consistente e reutilizável

### Dimensões
- `dim_player`
- `dim_game`
- `dim_championship`
- `dim_round`

### Fato
- `fact_player_game_stats`
  - Grain: 1 jogador × 1 jogo
  - Métricas atômicas

### Ferramenta
- `dbt Core`
- Transformações declarativas (SQL)
- Testes:
  - `not_null`
  - `unique`
  - `relationships`

---

## 5. Camada GOLD — Tabelas Analíticas
**Objetivo:** otimizar consultas para dashboards e métricas de negócio

### Exemplos de Tabelas
- `gold_player_season_stats`
- `gold_team_leaderboards`
- `gold_match_summary`
- `gold_championship_kpis`

### Características
- Dados já agregados
- Regras de negócio consolidadas
- Leitura rápida (baixo custo computacional)

---

## 6. Orquestração e Automação
- `dbt Core` executado via GitHub Actions
- Gatilhos:
  - Novo upload de dados
  - Execução manual
- Logs versionados
- Reprocessamento idempotente

---

## 7. Front-end — Streamlit
- Conecta **apenas** ao schema `gold`
- Dashboards:
  - Ranking de jogadores
  - Estatísticas por jogo
  - Evolução temporal
  - Comparações

---

## 8. Deploy
- Streamlit Community Cloud
- Neon Free Tier
- GitHub como single source of truth

---

# 2️⃣ Fluxo do Produto Final — Visão do Cliente

## 👤 Perfil do Usuário
- Organizador do campeonato
- Jogadores
- Público interessado em estatísticas

---

## 🔁 Ciclo de Uso do Sistema

### 1. Upload de Dados
- Admin acessa o painel
- Faz upload da planilha do campeonato
- Sistema valida e salva os dados brutos

---

### 2. Processamento Automático
- Pipeline é acionado automaticamente
- Dados são:
  - Organizados
  - Normalizados
  - Modelados em Star Schema
  - Agregados para análises

---

### 3. Consumo Analítico
- Usuários acessam o app Streamlit
- Visualizam:
  - Rankings atualizados
  - Estatísticas por jogador e jogo
  - KPIs do campeonato
- Sem atrasos, sem cálculos no front-end

---

## 🧠 O Que o Cliente Ganha

- Dados confiáveis e auditáveis
- Atualizações simples (apenas subir a planilha)
- Métricas consistentes
- Interface clara e rápida
- Arquitetura moderna, escalável e sem custo

---

## 🧩 Diferencial Técnico
- Arquitetura em camadas (RAW / SILVER / GOLD)
- Modelagem dimensional explícita
- dbt como motor central de transformação
- Serverless real (Neon + Streamlit)

---

📌 **Resumo Final:**  
O usuário só interage com **planilhas e dashboards**, enquanto toda a complexidade de engenharia de dados fica encapsulada em uma arquitetura robusta, reproduzível e profissional.
