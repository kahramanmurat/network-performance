{{ config(materialized='table') }}

with nw_data as (
    select * from {{ ref('fact_nw_data') }}
)
    select 
    siteid,
    date,
    sitename,
    statename,

    -- Performance calculation 
    sum(rrc_enum) as rrc_enum_daily,
    sum(rrc_denom) as rrc_denom_daily,
    sum(erab_enum) as erab_enum_daily,
    sum(erab_denom) as erab_denom_daily,
    sum(rtp_gap_enum) as rtp_gap_enum_daily,
    sum(rtp_gap_denom) as rtp_gap_denom_daily,
    sum(sip_dc_enum) as sip_dc_enum_daily,
    sum(sip_dc_denom) as sip_dc_denom_daily,
    sum(volte_ia_enum) as volte_ia_enum_daily,
    sum(volte_ia_denom) as volte_ia_denom_daily,
    sum(ho_enum) as ho_enum_daily,
    sum(ho_denom) as ho_denom_daily,
    sum(dl_traffic) as dl_traffic_daily,
    sum(ul_traffic) as ul_traffic_daily,

    -- Additional calculations
    avg(dl_user_throughput) as avg_dl_user_throughput_daily,
    avg(ul_user_throughput) as avg_ul_user_throughput_daily,
    avg(average_user) as average_user_daily,
    max(max_user) as max_user_daily

    from nw_data
    group by 1,2,3,4