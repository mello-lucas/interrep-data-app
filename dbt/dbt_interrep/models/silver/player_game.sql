{{ config(materialized="table") }}

with ranked as (

    select
        ingestion_id,
        ingested_at,
        date,
        championship,
        round,
        team,
        name,
        nickname,
        goals,
        own_goals,
        assists,
        yellow_cards,
        blue_cards,
        red_cards,
        saves,

        row_number() over (
            partition by
                date,
                championship,
                round,
                team,
                name
            order by ingested_at desc
        ) as rn

    from {{ source("raw", "player_game_ingest") }}

)

select
    ingestion_id,
    ingested_at,
    date,
    championship,
    round,
    team,
    name,
    nickname,
    goals,
    own_goals,
    assists,
    yellow_cards,
    blue_cards,
    red_cards,
    saves
from ranked
where rn = 1
