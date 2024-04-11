with source as 

(
  select *,
    row_number() over(partition by site, timestamp) as rn
  from {{ source('staging','table_2021') }}
  where site is not null 
),

renamed as (

    select
        {{ dbt_utils.generate_surrogate_key(['site', 'county']) }} as siteid,
        -- timestamps
        cast(timestamp as timestamp) as datetime,
        DATE(timestamp) as date,
        TIME(timestamp) as time,
        EXTRACT(YEAR from timestamp) as year,
        EXTRACT(MONTH from timestamp) as month,
        EXTRACT(DAY from timestamp) as day,

        cast(site as string) as sitename,
        cast(county as string) as statename,

        -- raw counters
        cast(rrc_enum as numeric) as rrc_enum,
        cast(rrc_denom as numeric) as rrc_denom,
        cast(erab_enum as numeric) as erab_enum,
        cast(erab_denom as numeric) as erab_denom,

        cast(rtp_gap_enum as numeric) as rtp_gap_enum,
        cast(rtp_gap_denom as numeric) as rtp_gap_denom,
        cast(sip_dc_enum as numeric) as sip_dc_enum,
        cast(sip_dc_denom as numeric) as sip_dc_denom,
        cast(ho_denom as numeric) as ho_denom,
        cast(ho_enum as numeric) as ho_enum,

        cast(volte_ia_enum as numeric) as volte_ia_enum,
        cast(volte_ia_denom as numeric) as volte_ia_denom,

        cast(dl_user_throughput as decimal) as dl_user_throughput,
        cast(ul_user_throughput as decimal) as ul_user_throughput,

        cast(dl_traffic as decimal) as dl_traffic,
        cast(ul_traffic as decimal) as ul_traffic,

        cast(max_user as decimal) as max_user,
        cast(average_user as decimal) as average_user

    from source
    where rn = 1

)

select * from renamed

-- dbt build --select stg_table_2020 --vars '{'is_test_run': 'false'}'
-- dbt build --select stg_table_2020 
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}