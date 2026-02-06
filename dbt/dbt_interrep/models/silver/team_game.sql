{{ config(materialized="table") }}

WITH base AS (
    SELECT
        ingestion_id,
        date,
        championship,
        round,
        team,
        SUM(goals) AS goals,
        SUM(own_goals) AS own_goals
    FROM
        {{ ref("player_game") }}
    GROUP BY
        ingestion_id,
        date,
        championship,
        round,
        team
),

paired AS (
    SELECT
        a.ingestion_id,
        a.championship,
        a.round,
        a.date,
        a.team,
        b.team AS team_opponent,
        a.goals + b.own_goals AS goals_scored,
        b.goals + a.own_goals AS goals_conceded
    FROM base a
    LEFT JOIN base b
    ON a.ingestion_id = b.ingestion_id
    AND a.team <> b.team
)

SELECT
    *,
    goals_scored - goals_conceded AS goal_diff
FROM
    paired