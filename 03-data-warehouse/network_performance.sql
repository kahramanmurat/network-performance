-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `network-performance-418402.network_performance.external_all_years`
OPTIONS (
  format = 'CSV',
  uris = ['gs://network-performance-418402-bucket/2020/*.csv', 'gs://network-performance-418402-bucket/2021/*.csv', 
  'gs://network-performance-418402-bucket/2022/*.csv', 'gs://network-performance-418402-bucket/2023/*.csv', 
  'gs://network-performance-418402-bucket/2024/*.csv']
);

-- Check performance data
SELECT * FROM network-performance-418402.network_performance.external_all_years limit 10;


-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE network-performance-418402.network_performance.performance_data_non_partitoned AS
SELECT * FROM network-performance-418402.network_performance.external_all_years;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE network-performance-418402.network_performance.performance_data_partitoned
PARTITION BY
  DATE(timestamp) AS
SELECT * FROM network-performance-418402.network_performance.external_all_years;

-- Impact of partition
-- Scanning 1.58GB of data
SELECT DISTINCT(site)
FROM network-performance-418402.network_performance.performance_data_non_partitoned
WHERE DATE(timestamp) BETWEEN '2020-06-01' AND '2020-06-30';

-- Scanning ~31.17 MB of DATA
SELECT DISTINCT(site)
FROM network-performance-418402.network_performance.performance_data_partitoned
WHERE DATE(timestamp) BETWEEN '2020-06-01' AND '2020-06-30';


-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `network_performance.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'network-performance-418402.network_performance.performance_data_partitoned'
ORDER BY total_rows DESC;


-- Creating a partition and cluster table
CREATE OR REPLACE TABLE network-performance-418402.network_performance.performance_partitoned_clustered
PARTITION BY DATE(timestamp)
CLUSTER BY site AS
SELECT * FROM network-performance-418402.network_performance.external_all_years;

-- Query scans 601.6 MB
SELECT count(*) as counts
FROM network-performance-418402.network_performance.performance_data_partitoned
WHERE DATE(timestamp) BETWEEN '2020-06-01' AND '2021-12-31'
  AND site='Mary Path';

-- Query scans 601.6 MB
SELECT count(*) as counts
FROM network-performance-418402.network_performance.performance_partitoned_clustered
WHERE DATE(timestamp) BETWEEN '2020-06-01' AND '2021-12-31'
  AND site='Mary Path';