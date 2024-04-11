{{ config(materialized='table') }}

with nw_data as (
    select * from {{ ref('fact_nw_data') }}
)
    select 
    siteid,
    year,
    month,
    sitename,
    statename,

    -- Performance calculation 
    sum(rrc_enum) as rrc_enum_monthly,
    sum(rrc_denom) as rrc_denom_monthly,
    sum(erab_enum) as erab_enum_monthly,
    sum(erab_denom) as erab_denom_monthly,
    sum(rtp_gap_enum) as rtp_gap_enum_monthly,
    sum(rtp_gap_denom) as rtp_gap_denom_monthly,
    sum(sip_dc_enum) as sip_dc_enum_monthly,
    sum(sip_dc_denom) as sip_dc_denom_monthly,
    sum(volte_ia_enum) as volte_ia_enum_monthly,
    sum(volte_ia_denom) as volte_ia_denom_monthly,
    sum(ho_enum) as ho_enum_monthly,
    sum(ho_denom) as ho_denom_monthly,
    sum(dl_traffic) as dl_traffic_monthly,
    sum(ul_traffic) as ul_traffic_monthly,

    -- Additional calculations
    avg(dl_user_throughput) as avg_dl_user_throughput_monthly,
    avg(ul_user_throughput) as avg_ul_user_throughput_monthly,
    avg(average_user) as average_user_monthly,
    max(max_user) as max_user_monthly

    from nw_data
    group by 1,2,3,4,5