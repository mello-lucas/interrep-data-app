{{ config(materialized="table") }}

WITH base AS (
    SELECT
        *,
        ROW_NUMBER() OVER(
            PARTITION BY ingestion_id
            ORDER BY team
        ) AS rn
    FROM
        {{ ref("team_game") }}
)

SELECT
    championship,
    round,
    date,
    team,
    team_opponent,
    goals_scored,
    goals_conceded
FROM
    base
WHERE
    rn = 1