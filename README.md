# Network Performance Project

This folder contains my project for the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by [DataTalks.Club](https://datatalks.club).

## Index
- [Network Performance Project](#network-performance)
  - [Index](#index)
- [Problem](#problem)
- [Dataset](#dataset)
- [Dashboard](#dashboard)
- [Project details and implementation](#project-details-and-implementation)
- [Reproduce the project](#reproduce-the-project)
  - [Prerequisites](#prerequisites)
  - [Create a Google Cloud Project](#create-a-google-cloud-project)
  - [Creating an environment variable for the credentials](#creating-an-environment-variable-for-the-credentials)
  - [Install and setup Google Cloud SDK](#install-and-setup-google-cloud-sdk)
  - [Create a VM instance](#create-a-vm-instance)
    - [Using the GCP dashboard](#using-the-gcp-dashboard)
    - [Using the SDK](#using-the-sdk)
  - [Set up SSH access to the VM](#set-up-ssh-access-to-the-vm)
  - [Starting and stopping your instance with gcloud sdk after you shut it down](#starting-and-stopping-your-instance-with-gcloud-sdk-after-you-shut-it-down)
  - [Installing the required software in the VM](#installing-the-required-software-in-the-vm)
    - [Docker:](#docker)
    - [Docker compose:](#docker-compose)
    - [Terraform:](#terraform)
    - [Google credentials](#google-credentials)
  - [Upload/download files to/from your instance](#uploaddownload-files-tofrom-your-instance)
  - [Clone the repo in the VM](#clone-the-repo-in-the-vm)
  - [Set up project infrastructure with Terraform](#set-up-project-infrastructure-with-terraform)
  - [Set up data ingestion with Airflow](#set-up-data-ingestion-with-airflow)
  - [Perform the data ingestion](#perform-the-data-ingestion)
  - [Setting up dbt Cloud](#setting-up-dbt-cloud)
  - [Deploying models in dbt Cloud with a Production environment](#deploying-models-in-dbt-cloud-with-a-production-environment)
  - [Creating a dashboard](#creating-a-dashboard)

# Problem

The primary objective of this project is to develop a solution that effectively handles and transforms network performance data, specifically focusing on Downlink and Uplink data traffic. This data, though artificially generated, will be stored in a designated GitHub repository. The transformation process will aim to prepare the data for subsequent visual analysis, facilitating both monthly and yearly overviews of traffic trends on a daily basis.

The challenge involves retrieving the raw data, ensuring its accuracy and suitability for analysis, and then applying data transformation techniques to enable clear and comprehensive visual representations. This will involve calculating aggregates, averages, and possibly other statistical measures to represent the data effectively across different time frames.

The ultimate goal is to provide stakeholders with insights into network performance trends, helping in strategic decision-making and operational adjustments based on data-driven evidence. This project will leverage programming and data processing skills to achieve a robust analytical tool that enhances the understanding of network dynamics over time.

# Dataset

The dataset utilized in this project is hosted on GitHub in the repository found at this link [GitHub Folder](https://github.com/kahramanmurat/network-performance-data). This dataset comprises artificially generated network performance data, meticulously designed to simulate real-world network traffic conditions. The data encompasses a period from the start of 2020 up to April 11, 2024, providing a comprehensive view of network dynamics over an extended timeframe.

The data generation process is scripted in Python and can be reviewed via the code provided in a related repository [code](https://github.com/kahramanmurat/network-performance/blob/main/01-docker-terraform/2_docker_sql/main10.py). 

The dataset includes key performance indicators such as Downlink and Uplink data traffic volumes, recorded daily. This allows for detailed analysis and visualization of data trends on both a monthly and yearly basis. The structured nature of the dataset, combined with its accessibility via GitHub, ensures that it is readily usable for processing and analysis in the project. This dataset is instrumental for analyzing trends, identifying performance issues, and evaluating the efficiency of network systems over time.

# Dashboard

You may access the dashboard with the visualizations [in this link](https://lookerstudio.google.com/reporting/f31333e5-a787-45ba-98c1-a2be8dd94399).

# Project details and implementation

This project leverages the Google Cloud Platform (GCP) to manage and analyze network performance data. Key GCP services utilized include Cloud Storage and BigQuery, which serve as the foundation for storing and querying large datasets effectively. The cloud infrastructure, including the configuration and deployment of services, is predominantly handled using Terraform. This provides a structured and reproducible method for infrastructure deployment. However, the management of Airflow and dbt instances is detailed separately, highlighting their specific configurations and roles within the project.

Data ingestion is automated through an Apache Airflow Directed Acyclic Graph (DAG). This DAG is scheduled to run daily, performing the following tasks:

Data Download: It fetches new dataset updates in CSV format from a specified source.
Data Transformation: Before storage, the DAG processes the CSV files to strip any unnecessary payload objects that are not needed for analysis.
Data Storage: Post-transformation, the data is uploaded to a Google Cloud Storage bucket, which acts as the Data Lake of the project.
External Table Creation: Additionally, the DAG configures an external table in BigQuery, enabling efficient querying of the stored data, which is now in Parquet format for optimized performance.

The Data Warehouse architecture is designed and maintained using dbt (data build tool), which allows for the creation of complex data models with ease:

Table Configuration: dbt is used to create a comprehensive table from the CSV data, which is partitioned by timestamps and clustered by site locations to enhance query performance.
Transformation Logic: dbt also manages the data transformation logic necessary for downstream analysis and visualization, ensuring data is in the optimal format.

The final component of the project is a visualization dashboard created using Google Data Studio. This dashboard includes four key widgets, designed to provide intuitive and actionable insights into network performance data:

Widgets Overview: Each widget focuses on different aspects of the data, such as daily traffic trends, comparative monthly or yearly analysis, and peak traffic times, all tailored from data ranging between 2020 to April 11, 2024.
User Interaction: The dashboard is structured to be user-friendly, allowing stakeholders to easily navigate through various data points and extract meaningful information relevant to their specific needs.



