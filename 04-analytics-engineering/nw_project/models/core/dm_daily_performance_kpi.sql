{{ config(materialized='table') }}

with nw_data as (
    select * from {{ ref('dm_daily_performance') }}
)
    select 
    siteid,
    date,
    sitename,
    statename,

    -- Performance calculation 

    ROUND((SUM(rrc_enum_daily) / NULLIF(SUM(rrc_denom_daily), 0)) * 100, 2) AS rrc_sr_daily,
    ROUND((SUM(erab_enum_daily) / NULLIF(SUM(erab_denom_daily), 0)) * 100, 2) AS erab_sr_daily,
    ROUND((SUM(rtp_gap_enum_daily) / NULLIF(SUM(rtp_gap_denom_daily), 0)) * 100, 2) AS rtp_gap_sr_daily,
    ROUND((SUM(sip_dc_enum_daily) / NULLIF(SUM(sip_dc_denom_daily), 0)) * 100, 2) AS sip_dc_sr_daily,
    ROUND((SUM(volte_ia_enum_daily) / NULLIF(SUM(volte_ia_denom_daily), 0)) * 100, 2) AS volte_ia_sr_daily,
    ROUND((SUM(ho_enum_daily) / NULLIF(SUM(ho_denom_daily), 0)) * 100, 2) AS ho_sr_daily,
    ROUND(SUM(dl_traffic_daily), 2) AS dl_traffic_daily,
    ROUND(SUM(ul_traffic_daily), 2) AS ul_traffic_daily,
    ROUND(AVG(avg_dl_user_throughput_daily), 2) AS avg_dl_user_throughput_daily,
    ROUND(AVG(avg_ul_user_throughput_daily), 2) AS avg_ul_user_throughput_daily,
    ROUND(AVG(average_user_daily), 2) AS average_user_daily,
    ROUND(MAX(max_user_daily), 2) AS max_user_daily

    from nw_data
    group by 1,2,3,4