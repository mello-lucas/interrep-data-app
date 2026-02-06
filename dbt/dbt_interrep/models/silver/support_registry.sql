{{ config(materialized="table") }}

with ranked as (

    select
        ingestion_id,
        ingested_at,
        year,
        championship,
        team,
        name,
        nickname,

        row_number() over (
            partition by
                year,
                championship,
                team,
                name
            order by ingested_at desc
        ) as rn

    from {{ source("raw", "support_registry") }}

)

select
    ingestion_id,
    ingested_at,
    year,
    championship,
    team,
    name,
    nickname
from ranked
where rn = 1
