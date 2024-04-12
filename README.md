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

# Reproduce the project

## Prerequisites

The following requirements are needed to reproduce the project:

1. A [Google Cloud Platform](https://cloud.google.com/) account.
2. (Optional) The [Google Cloud SDK](https://cloud.google.com/sdk). Instructions for installing it are below.
    * Most instructions below will assume that you are using the SDK for simplicity.
3. (Optional) A SSH client.
    * All the instructions listed below assume that you are using a Terminal and SSH.
4. (Optional) VSCode with the Remote-SSH extension.
    * Any other IDE should work, but VSCode makes it very convenient to forward ports in remote VM's.

## Create a Google Cloud Project

Access the [Google Cloud dashboard](https://console.cloud.google.com/) and create a new project from the dropdown menu on the top left of the screen, to the right of the _Google Cloud Platform_ text.

After you create the project, you will need to create a _Service Account_ with the following roles:
* `BigQuery Admin`
* `Storage Admin`
* `Storage Object Admin`
* `Viewer`

Download the Service Account credentials file, rename it to `google_credentials.json` and store it in your home folder, in `$HOME/.google/credentials/` .
> ***IMPORTANT***: if you're using a VM as recommended, you will have to upload this credentials file to the VM.


You will also need to activate the following APIs:
* https://console.cloud.google.com/apis/library/iam.googleapis.com
* https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

If all of these steps are unfamiliar to you, please review [Lesson 1.3.1 - Introduction to Terraform Concepts & GCP Pre-Requisites (YouTube)](https://youtu.be/Hajwnmj0xfQ?t=198), or check out my notes [here](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/1_intro.md#gcp-initial-setup).

## Creating an environment variable for the credentials

Create an environment variable called `GOOGLE_APPLICATION_CREDENTIALS` and assign it to the path of your json credentials file, which should be `$HOME/.google/credentials/` . Assuming you're running bash:

1. Open `.bashrc`:
    ```sh
    nano ~/.bashrc
    ```
1. At the end of the file, add the following line:
    ```sh
    export GOOGLE_APPLICATION_CREDENTIALS="<path/to/authkeys>.json"
    ```
1. Exit nano with `Ctrl+X`. Follow the on-screen instructions to save the file and exit.
1. Log out of your current terminal session and log back in, or run `source ~/.bashrc` to activate the environment variable.
1. Refresh the token and verify the authentication with the GCP SDK:
    ```sh
    gcloud auth application-default login
    ```

## Install and setup Google Cloud SDK

1. Download Gcloud SDK [from this link](https://cloud.google.com/sdk/docs/install) and install it according to the instructions for your OS.
1. Initialize the SDK [following these instructions](https://cloud.google.com/sdk/docs/quickstart).
    1. Run `gcloud init` from a terminal and follow the instructions.
    1. Make sure that your project is selected with the command `gcloud config list`

## Create a VM instance

### Using the GCP dashboard

1. From your project's dashboard, go to _Cloud Compute_ > _VM instance_
1. Create a new instance:
    * Any name of your choosing
    * Pick your favourite region. You can check out the regions [in this link](https://cloud.google.com/about/locations).
        > ***IMPORTANT***: make sure that you use the same region for all of your Google Cloud components.
    * Pick a _E2 series_ instance. A _e2-standard-4_ instance is recommended (4 vCPUs, 16GB RAM)
    * Change the boot disk to _Ubuntu_. The _Ubuntu 20.04 LTS_ version is recommended. Also pick at least 30GB of storage.
    * Leave all other settings on their default value and click on _Create_.

### Using the SDK

The following command will create a VM using the recommended settings from above. Make sure that the region matches your choice:

```sh
gcloud compute instances create <name-of-the-vm> --zone=<google-cloud-zone> --image-family=ubuntu-2004-lts --image-project=ubuntu-os-cloud --machine-type=e2-standard-4 --boot-disk-size=30GB
```


## Set up SSH access to the VM

1. Start your instance from the _VM instances_ dashboard in Google Cloud.
1. In your local terminal, make sure that the gcloud SDK is configured for your project. Use `gcloud config list` to list your current config's details.
    1. If you have multiple google accounts but the current config does not match the account you want:
        1. Use `gcloud config configurations list` to see all of the available configs and their associated accounts.
        1. Change to the config you want with `gcloud config configurations activate my-project`
    1. If the config matches your account but points to a different project:
        1. Use `gcloud projects list` to list the projects available to your account (it can take a while to load).
        1. use `gcloud config set project my-project` to change your current config to your project.
3. Set up the SSH connection to your VM instances with `gcloud compute config-ssh`
    * Inside `~/ssh/` a new `config` file should appear with the necessary info to connect.
    * If you did not have a SSH key, a pair of public and private SSH keys will be generated for you.
    * The output of this command will give you the _host name_ of your instance in this format: `instance.zone.project` ; write it down.
4. You should now be able to open a terminal and SSH to your VM instance like this:
   * `ssh instance.zone.project`
5. In VSCode, with the Remote SSH extension, if you run the [command palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette) and look for _Remote-SSH: Connect to Host_ (or alternatively you click on the Remote SSH icon on the bottom left corner and click on _Connect to Host_), your instance should now be listed. Select it to connect to it and work remotely.

## Starting and stopping your instance with gcloud sdk after you shut it down (OPTIONAL)

1. List your available instances.
    ```sh
    gcloud compute instances list
    ```
1. Start your instance.
    ```sh
    gcloud compute instances start <instance_name>
    ```
1. Set up ssh so that you don't have to manually change the IP in your config files.
    ```sh
    gcloud compute config-ssh
    ```
1. Once you're done working with the VM, you may shut it down to avoid consuming credit.
    ```sh
    gcloud compute instances stop <instance_name>


## Installing the required software in the VM

1. Run this first in your SSH session: `sudo apt update && sudo apt -y upgrade`
    * It's a good idea to run this command often, once per day or every few days, to keep your VM up to date.
### Docker:
1. Run `sudo apt install docker.io` to install it.
1. Change your settings so that you can run Docker without `sudo`:
    1. Run `sudo groupadd docker`
    1. Run `sudo gpasswd -a $USER docker`
    1. Log out of your SSH session and log back in.
    1. Run `sudo service docker restart`
    1. Test that Docker can run successfully with `docker run hello-world`
### Docker compose:
1. Go to https://github.com/docker/compose/releases and copy the URL for the  `docker-compose-linux-x86_64` binary for its latest version.
    * At the time of writing, the last available version is `v2.2.3` and the URL for it is https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64
1. Create a folder for binary files for your Linux user:
    1. Create a subfolder `bin` in your home account with `mkdir ~/bin`
    1. Go to the folder with `cd ~/bin`
1. Download the binary file with `wget <compose_url> -O docker-compose`
    * If you forget to add the `-O` option, you can rename the file with `mv <long_filename> docker-compose`
    * Make sure that the `docker-compose` file is in the folder with `ls`
1. Make the binary executable with `chmod +x docker-compose`
    * Check the file with `ls` again; it should now be colored green. You should now be able to run it with `./docker-compose version`
1. Go back to the home folder with `cd ~`
1. Run `nano .bashrc` to modify your path environment variable:
    1. Scroll to the end of the file
    1. Add this line at the end:
       ```bash
        export PATH="${HOME}/bin:${PATH}"
        ```
    1. Press `CTRL` + `o` in your keyboard and press Enter afterwards to save the file.
    1. Press `CTRL` + `x` in your keyboard to exit the Nano editor.
1. Reload the path environment variable with `source .bashrc`
1. You should now be able to run Docker compose from anywhere; test it with `docker-compose version`
### Terraform:
1. Run `curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -`
1. Run `sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"`
1. Run `sudo apt-get update && sudo apt-get install terraform`

### Google credentials

Make sure that you upload the `google_credentials.json` to `$HOME/.google/credentials/` and you create the `GOOGLE_APPLICATION_CREDENTIALS` as specified in the _Creating an environment variable for the credentials_ section.


## Upload/download files to/from your instance

1. Download a file.
    ```sh
    # From your local machine
    scp <instance_name>:path/to/remote/file path/to/local/file
    ```

1. Upload a file.
    ```sh
    # From your local machine
    scp path/to/local/file <instance_name>:path/to/remote/file
    ```

1. You can also drag & drop stuff in VSCode with the remote extension.

2. If you use a client like Cyberduck, you can connect with SFTP to your instance using the `instance.zone.project` name as server, and adding the generated private ssh key.

## Clone the repo in the VM

Log in to your VM instance and run the following from your `$HOME` folder:

```sh
git clone https://github.com/kahramanmurat/network-performance.git
```

## Set up project infrastructure with Terraform

Make sure that the credentials are updated and the environment variable is set up.

1. Go to the `network-performance/01-docker-terraform/1_terraform_gcp/terraform` folder.

2. Open `variables.tf` and edit line 11 under the `variable "region"` block so that it matches your preferred region.

3. Initialize Terraform:
    ```sh
    terraform init
    ```
4. Plan the infrastructure and make sure that you're creating a bucket in Cloud Storage as well as a dataset in BigQuery
    ```sh
    terraform plan
    ```
5. If the plan details are as expected, apply the changes.
    ```sh
    terraform apply
    ```

You should now have a bucket called `network-performance-418402-bucket` and a dataset called `network_performance` in BigQuery.

## Set up data ingestion with Airflow

1. Go to the `network-performance/02-workflow-orchestration/airflow` folder.

2. Run the following command and write down the output:
    ```sh
    echo -e "AIRFLOW_UID=$(id -u)"
    ```
3. Open the `.env` file and change the value of `AIRFLOW_UID` for the value of the previous command.
4. Change the value of `GCP_PROJECT_ID` for the name of your project id in Google Cloud and also change the value of `GCP_GCS_BUCKET` for the name of your bucket.
5. Build the custom Airflow Docker image:
    ```sh
    docker-compose build
    ```
1. Initialize the Airflow configs:
    ```sh
    docker-compose up airflow-init
    ```
1. Run Airflow
    ```sh
    docker-compose up
    ```

You may now access the Airflow GUI by browsing to `localhost:8080`. Username and password are both `airflow` .
>***IMPORTANT***: this is ***NOT*** a production-ready setup! The username and password for Airflow have not been modified in any way; you can find them by searching for `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD` inside the `docker-compose.yaml` file.

## Perform the data ingestion

If you performed all the steps of the previous section, you should now have a web browser with the Airflow dashboard.

The DAG is set up to download all data starting from April 1st 2022. You may change this date by modifying line 202 of `network-performance/02-workflow-orchestration/airflow/data_ingestion_gcs_dag.py`. 

To trigger the DAG, simply click on the switch icon next to the DAG name. The DAG will retrieve all data from the starting date to the latest available hour and then perform hourly checks on every 30 minute mark.

After the data ingestion, you may shut down Airflow by pressing `Ctrl+C` on the terminal running Airflow and then running `docker-compose down`, or you may keep Airflow running if you want to update the dataset every hour. If you shut down Airflow, you may also shut down the VM instance because it won't be needed for the following steps.

## Setting up dbt Cloud

1. Create a [dbt CLoud account](https://www.getdbt.com/).
1. Create a new project.
    1. Give it a name (`network-performance-analytics` is recommended), and under _Advanced settings_, input `04-analytics-engineering/nw_project` as the _Project subdirectory_.
    1. Choose _BigQuery_ as a database connection.
    1. Choose the following settings:
        * You may leave the default connection name.
        * Upload a Service Account JSON file > choose the `google_credentials.json` we created previously.
        * Under _BigQuery Optional Settings_, make sure that you put your Google Cloud location under _Location_.
        * Under _Development credentials_, choose any name for the dataset. This name will be added as a prefix to the schemas. In this project the name `dbt` was used.
        * Test the connection and click on _Continue_ once the connection is tested successfully.
    1. In the _Add repository from_ form, click on Github and choose your fork from your user account. Alternatively, you may provide a URL and clone the repo.
1. Once the project has been created, you should now be able to click on the hamburger menu on the top left and click on _Develop_ to load the dbt Cloud IDE.

You may now run the `dbt run` command in the bottom prompt to run all models; this will generate 3 different datasets in BigQuery:
* `<prefix>_staging` hosts the staging views for generating the final end-user tables.
* `<prefix>_core` hosts the end-user tables.

## Deploying models in dbt Cloud with a Production environment

1. Click on the hamburger menu on the top left and click on _Environments_.
1. Click on the _New Environment_ button on the top right.
1. Give the environment a name (`Production` is recommended), make sure that the environment is of type _Deployment_ and in the _Credentials_ section, you may input a name in the _Dataset_ field; this will add a prefix to the schemas, similarly to what we did in when setting up the development environment (`production` is the recommended prefix but any prefix will do, or you may leave it blank).
1. Create a new job with the following settings:
    * Give it any name; `dbt run` is recommended.
    * Choose the environment you created in the previous step.
    * Optionally, you may click on the _Generate docs?_ checkbox.
    * In the _Commands_ section, add the command `dbt run`
    * In the _Triggers_ section, inside the _Schedule_ tab, make sure that the _Run on schedule?_ checkbox is checked. Select _custom cron schedule_ and input the string `40 * * * *`; this will run the models every hour on the 40th minute (the DAG runs on the 30th minute, the 10 minute delay is to make sure that the DAG is run successfully).
1. Save the job.

You may now trigger the job manually or you may wait until the scheduled trigger to run it. The first time you run it, 10 new datasets will be added to BigQuery following the same pattern as in the development environment.

## Creating a dashboard

The dashboard used in this project was generated with [Google Data Studio](https://lookerstudio.google.com/) (GDS from now on). Dashboards in GDS are called _reports_. Reports grab data from _data sources_. We will need to generate 2 data sources and a report:

1. Generate the data sources.
    1. Click on the _Create_ button and choose _Data source_.
    2. Click on the _BigQuery_ connector.
    3. Choose your Google Cloud project, choose your `prod`  dataset and click on the `fact_nw_data` table. Click on the _Connect_ button at the top.
    4. You may rename the data source by clicking on the name at the top left of the screen. The default name will be the name of the chosen table.
2. Generate the report.
    1. Click on the _Create_ button and choose _Report_.
    2. If the _Add data to report_ pop-up appears, choose the `My data sources` tab and choose one of the data sources. Click on the _Add to report_ button on the confirmation pop-up.
    3. Once you're in the report page, click on the _Add data_ button on the top bar and choose the other data source you created.
    4.  You may delete any default widgets created by GDS.
3. Add the _Monthly DL Traffic per Year_ widget.

4. Add the _Monthly DL Traffic per Year_ widget.


You should now have a functioning dashboard.

_[Back to the repo index](https://github.com/kahramanmurat/network-performance)_