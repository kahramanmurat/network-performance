{{
    config(
        materialized='table'
    )
}}

with table_2020 as (
    select *
    from {{ ref('stg_table_2020') }}
), 

    table_2021 as (
    select *
    from {{ ref('stg_table_2021') }}
), 

    table_2022 as (
    select *
    from {{ ref('stg_table_2022') }}
), 


    table_2023 as (
    select *
    from {{ ref('stg_table_2023') }}
), 

    table_2024 as (
    select *
    from {{ ref('stg_table_2024') }}
), 

    table_unioned as (
    select * from table_2020
    union all 
    select * from table_2021
    union all
    select * from table_2022 
    union all
    select * from table_2023
    union all
    select * from table_2024 
)

select * from table_unioned