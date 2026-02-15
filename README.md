# Interrep — Data App

Aplicação em Streamlit para acompanhamento do Torneio Interrep, com ingestão de planilhas (`.xlsx`), transformação em camadas de dados e consumo analítico em dashboards.

## Visão Geral

O projeto segue um fluxo simples:

1. Admin faz upload da planilha do jogo.
2. O arquivo passa por validações estruturais e semânticas.
3. Os dados são gravados em modo append-only na camada RAW.
4. Um workflow de `dbt build` pode ser disparado pela aba Admin.
5. As páginas analíticas leem tabelas prontas da camada GOLD.

## Stack

- Frontend: Streamlit
- Ingestão: Python + pandas
- Banco: PostgreSQL (Neon)
- Transformação: dbt Core (`dbt-postgres`)
- Orquestração de build: GitHub Actions

## Arquitetura de Dados

```text
Excel (.xlsx)
  -> raw.player_game_ingest
  -> dbt_silver.player_game
  -> dbt_silver.team_game
  -> dbt_gold.match_scoreboard
  -> dbt_gold.player_summary
  -> dbt_gold.team_summary
  -> Streamlit
```

### RAW

Tabela de entrada:
- `raw.player_game_ingest`

Características:
- append-only
- registra `ingestion_id` e `ingested_at`
- sem regras analíticas

### SILVER (dbt)

Modelos:
- `player_game` (deduplicação por jogo/time/jogador, mantendo registro mais recente)
- `team_game` (agregação por time e confronto)

### GOLD (dbt)

Modelos usados pela aplicação:
- `match_scoreboard` (placares por partida)
- `player_summary` (agregados por jogador/ano/campeonato/time)
- `team_summary` (agregados por time/ano/campeonato)

Observação: no ambiente atual do app, essas tabelas são lidas no schema `dbt_gold`.

## Funcionalidades da Aplicação

### Main (`main.py`)

- Configuração global da página
- Título e branding no sidebar

### Jogos (`pages/2_🏟️_Jogos.py`)

- Filtros por campeonato, rodada e time
- Tabela de partidas com placar e vencedor/empate
- Lista detalhada das partidas filtradas

### Times (`pages/3_🛡_Times.py`)

- Filtros por ano, campeonato e time
- KPIs do time (jogos, gols, assistências, cartões)
- Gráfico de artilharia (destaque do topo)
- Tabela com estatísticas individuais dos jogadores

### Rankings (`pages/4_🏆_Rankings.py`)

- Filtros globais por ano e campeonato
- Top 5 de jogadores por gols, assistências e defesas
- Tabela de classificação de times (Pts, J, V, E, D, GP, GC, SG)
- Destaques top 5 de ataque, defesa e saldo

### Sobre (`pages/5_ℹ️_Sobre.py`)

- Texto institucional do projeto

### Admin (`pages/6_🚧_Admin.py`)

- Proteção por senha (`ADMIN_PASSWORD`)
- Disparo manual do workflow de `dbt build`
- Upload de planilha `.xlsx`
- Validação de estrutura e conteúdo
- Preview dos dados parseados
- Confirmação de carga em `raw.player_game_ingest`

## Validações de Ingestão

### Estrutura de arquivo (`ingestion/validators_file.py`)

- arquivo Excel válido
- existência da aba `plan`
- mínimo de linhas do layout
- campos obrigatórios de cabeçalho/times

### Validação do DataFrame (`ingestion/validators_df.py`)

- colunas esperadas
- quantidade de linhas
- tipos numéricos inteiros e sem negativos
- tipo da coluna `date`
- exatamente 2 times por jogo
- `name` e `nickname` preenchidos

## Execução Local

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar secrets/variáveis

A aplicação busca primeiro em `st.secrets` e, na ausência, em variáveis de ambiente (`utils/secrets.py`).

Chaves usadas:
- `NEON_DATABASE_URL`
- `ADMIN_PASSWORD`
- `GITHUB_OWNER`
- `GITHUB_REPO`
- `GITHUB_WORKFLOW_FILE`
- `GITHUB_TOKEN`
- `GITHUB_REF` (opcional, padrão `main`)

### 3. Rodar app

```bash
streamlit run main.py
```

## Limites Atuais

- Não há CRUD de jogos no app.
- Não há edição de resultados históricos pela interface.
- O build dbt é disparado manualmente na aba Admin.
- Não há suíte de testes automatizados no repositório neste momento.
