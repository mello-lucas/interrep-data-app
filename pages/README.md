## Estrutura de Abas

A aplicação está organizada nas abas abaixo:

- Main
- Jogos
- Times
- Rankings
- Sobre
- Admin

---

## Main

### Propósito

Ponto de entrada e identidade visual da aplicação.

### Escopo atual

- Configuração global da página
- Título principal
- Logo no sidebar

### Fora do escopo atual

- KPIs globais
- Filtros analíticos

---

## Jogos

### Propósito

Visualizar partidas e resultados consolidados.

### Escopo atual

- Filtro por campeonato
- Filtro por rodada
- Filtro por time
- Tabela com jogo, placar e resultado (vitória/empate)
- Lista detalhada das partidas filtradas

### Características

- Dados read-only vindos de `dbt_gold.match_scoreboard`
- Sem edição de partidas

### Fora do escopo atual

- CRUD de jogos
- Agendamento/alteração manual de partidas

---

## Times

### Propósito

Analisar desempenho de um time e seus jogadores no período selecionado.

### Escopo atual

- Filtro por ano, campeonato e time
- KPIs de jogos, gols, assistências e cartões
- Ranking de gols com destaque para artilheiro
- Tabela de estatísticas por jogador

### Características

- Dados read-only de `dbt_gold.player_summary`
- Métricas agregadas por seleção de contexto

### Fora do escopo atual

- Comparações históricas multi-temporada
- Métricas avançadas (xG, etc.)

---

## Rankings

### Propósito

Exibir rankings consolidados de jogadores e tabela de times.

### Escopo atual

- Filtro por ano e campeonato
- Top 5 jogadores por gols, assistências e defesas
- Tabela de classificação de times (Pts, J, V, E, D, GP, GC, SG)
- Destaques top 5 de ataque, defesa e saldo

### Características

- Dados read-only de `dbt_gold.player_summary` e `dbt_gold.team_summary`
- Ordenação determinística

### Fora do escopo atual

- Rankings por posição/tipo de atleta
- Normalização por minuto

---

## Sobre

### Propósito

Apresentar contexto institucional do projeto.

### Escopo atual

- Descrição do Interrep
- Objetivo do produto
- Resumo do conteúdo disponível

---

## Admin

### Propósito

Executar operações administrativas de ingestão e atualização analítica.

### Escopo atual

- Autenticação por senha (`ADMIN_PASSWORD`)
- Disparo manual do pipeline de `dbt build` via GitHub Actions
- Upload de planilha Excel
- Validação estrutural e semântica
- Pré-visualização e confirmação de carga na RAW

### Características

- Área restrita
- Carga append-only em `raw.player_game_ingest`
