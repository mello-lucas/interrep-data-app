## 🗂️ Estrutura de Abas

A aplicação é organizada nas seguintes abas principais:

* Main
* Jogos
* Rankings
* Partidas
* Sobre
* Admin

Cada aba possui um escopo bem delimitado, descrito a seguir.

---

## 🏠 Main

### Propósito

Ponto de entrada da aplicação. Apresenta uma visão resumida do campeonato ativo.

### Escopo

* Seleção de campeonato (quando aplicável)
* KPIs simples e globais
* Visão geral do estado dos dados

### Conteúdos esperados

* Total de jogos
* Total de jogadores
* Total de gols
* Status do campeonato (em andamento / finalizado)

### Fora do escopo

* Análises temporais detalhadas
* Comparações avançadas
* Configurações

---

## ⚽ Jogos

### Propósito

Gerenciar e visualizar os **jogos como entidades centrais do sistema**.

### Escopo

* Listagem de jogos
* Visualização dos principais atributos
* Criação, edição e exclusão de jogos (CRUD)

### Conteúdos esperados

* Data do jogo
* Campeonato
* Rodada
* Times participantes
* Placar
* Status do jogo (agendado / realizado)

### Regras importantes

* Jogos são entidades **editáveis**
* Resultados e estatísticas derivam dos jogos, mas não são editados aqui

### Fora do escopo

* Estatísticas avançadas por jogo
* Histórico de alterações

---

## 🏆 Rankings

### Propósito

Exibir rankings consolidados de jogadores com base em métricas objetivas.

### Escopo

* Rankings simples e diretos
* Filtros básicos por campeonato

### Conteúdos esperados

* Ranking de gols
* Ranking de assistências
* Ranking de cartões

### Características

* Dados derivados (read-only)
* Ordenação clara e determinística
* Sem ajustes manuais

### Fora do escopo

* Rankings por posição
* Métricas normalizadas (por jogo, por minuto)
* Comparações entre jogadores

---

## 📋 Partidas

### Propósito

Detalhar o que aconteceu em cada jogo de forma estruturada.

### Escopo

* Visualização dos eventos por partida
* Resumo estatístico simples

### Conteúdos esperados

* Lista de jogadores que atuaram
* Gols, assistências e cartões por jogo
* Estatísticas agregadas básicas

### Características

* Dados totalmente derivados
* Somente leitura (append-only na origem)

### Fora do escopo

* Linha do tempo detalhada
* Eventos avançados (xG, mapas de calor)

---

## ℹ️ Sobre

### Propósito

Fornecer contexto institucional e técnico sobre o projeto.

### Escopo

* Explicação do que é o Interrep
* Público-alvo
* Visão geral do funcionamento dos dados

### Conteúdos esperados

* Descrição do projeto
* Frequência de atualização dos dados
* Limitações do MVP

### Fora do escopo

* Documentação técnica detalhada
* Roadmap completo

---

## 🔐 Admin

### Propósito

Área restrita para ingestão e manutenção dos dados.

### Escopo

* Upload de arquivos de dados
* Validações estruturais e semânticas
* Carga append-only na camada RAW

### Características

* Acesso restrito
* Operações administrativas apenas

### Fora do escopo

* Edição direta de resultados históricos
* Visualizações analíticas

---

## 🚧 Itens Explicitamente Fora do MVP

Os itens abaixo **não fazem parte do MVP**, mas são considerados evoluções naturais:

* Star Schema completo
* Métricas avançadas
* Comparações históricas profundas
* Auditoria detalhada
* Exportação de dados
* Dashboards exploratórios complexos

---

## 📌 Princípios de Design do MVP

* Simplicidade operacional
* Clareza semântica
* Dados confiáveis > dados sofisticados
* Preparação para crescimento sem refatoração
