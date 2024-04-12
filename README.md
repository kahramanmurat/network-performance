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

This is a simple project which takes data from the GitHub Archive and transforms it in order to visualize the top GitHub contributors as well as the amount of commits per day.
