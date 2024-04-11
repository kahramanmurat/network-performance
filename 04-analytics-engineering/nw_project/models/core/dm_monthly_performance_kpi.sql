{{ config(materialized='table') }}

with nw_data as (
    select * from {{ ref('dm_monthly_performance') }}
)
    select 
    siteid,
    year,
    month,
    sitename,
    statename,

    -- Performance calculation 

    ROUND((SUM(rrc_enum_monthly) / NULLIF(SUM(rrc_denom_monthly), 0)) * 100, 2) AS rrc_sr_monthly,
    ROUND((SUM(erab_enum_monthly) / NULLIF(SUM(erab_denom_monthly), 0)) * 100, 2) AS erab_sr_monthly,
    ROUND((SUM(rtp_gap_enum_monthly) / NULLIF(SUM(rtp_gap_denom_monthly), 0)) * 100, 2) AS rtp_gap_sr_monthly,
    ROUND((SUM(sip_dc_enum_monthly) / NULLIF(SUM(sip_dc_denom_monthly), 0)) * 100, 2) AS sip_dc_sr_monthly,
    ROUND((SUM(volte_ia_enum_monthly) / NULLIF(SUM(volte_ia_denom_monthly), 0)) * 100, 2) AS volte_ia_sr_monthly,
    ROUND((SUM(ho_enum_monthly) / NULLIF(SUM(ho_denom_monthly), 0)) * 100, 2) AS ho_sr_monthly,
    ROUND(SUM(dl_traffic_monthly), 2) AS dl_traffic_monthly,
    ROUND(SUM(ul_traffic_monthly), 2) AS ul_traffic_monthly,
    ROUND(AVG(avg_dl_user_throughput_monthly), 2) AS avg_dl_user_throughput_monthly,
    ROUND(AVG(avg_ul_user_throughput_monthly), 2) AS avg_ul_user_throughput_monthly,
    ROUND(AVG(average_user_monthly), 2) AS average_user_monthly,
    ROUND(MAX(max_user_monthly), 2) AS max_user_monthly

    from nw_data
    group by 1,2,3,4,5