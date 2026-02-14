{{ config(materialized="table") }}

WITH base AS (
    SELECT
        *,
        CASE 
            WHEN goal_diff > 0 THEN 'win'
            WHEN goal_diff < 0 THEN 'lose'
            ELSE 'draw'
        END AS result
    FROM 
        {{ ref("team_game") }}
)
SELECT
    EXTRACT(YEAR FROM date) AS year,
    championship,
    team,
    SUM(goals_scored) AS goals_scored,
    SUM(goals_conceded) AS goals_conceded,
    SUM(goal_diff) AS goals_diff,
    SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'lose' THEN 1 ELSE 0 END) AS losses,
    SUM(CASE WHEN result = 'draw' THEN 1 ELSE 0 END) AS draws,
    COUNT(*) AS games_qty
FROM base
GROUP BY 1, 2, 3