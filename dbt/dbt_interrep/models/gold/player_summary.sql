{{ config(materialized="table") }}

SELECT
    EXTRACT(YEAR FROM date) AS year,
    championship,
    team,
    name,
    nickname,

    SUM(goals) AS goals,
    SUM(own_goals) AS own_goals,
    SUM(assists) AS assists,
    SUM(yellow_cards) AS yellow_cards,
    SUM(blue_cards) AS blue_cards,
    SUM(red_cards) AS red_cards,
    SUM(saves) AS saves,

    COUNT(ingestion_id) AS games_qty,
    ROUND(AVG(goals), 3) AS goals_avg,
    SUM(goals + assists) AS goal_contributions,
    SUM(yellow_cards)
    + SUM(blue_cards) * 2
    + SUM(red_cards) * 3 AS indiscipline_score,
    COUNT(CASE WHEN goals > 0 THEN 1 END) AS games_with_goal
FROM
    {{ ref("player_game") }}
GROUP BY
    1, 2, 3, 4, 5