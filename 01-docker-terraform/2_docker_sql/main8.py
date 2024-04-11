import csv
import os
import random
from datetime import datetime, timedelta
import pandas as pd

def load_existing_sites_and_counties(file_path):
    """
    Reads an existing CSV file to extract and return unique site and county names.
    """
    data = pd.read_csv(file_path)
    sites_per_county = {}
    for index, row in data.iterrows():
        county = row['county']
        site = row['site']
        if county not in sites_per_county:
            sites_per_county[county] = []
        if site not in sites_per_county[county]:
            sites_per_county[county].append(site)
    return sites_per_county

def generate_hourly_data_for_new_range(sites_per_county, start_date, end_date):
    """
    Generates new hourly data for each site within each county for a specified date range.
    """
    while start_date <= end_date:
        year = start_date.year
        month = start_date.month
        day = start_date.day
        year_folder = f"data/{year}"
        month_folder = f"{year_folder}/{month:02d}"
        os.makedirs(month_folder, exist_ok=True)

        filename = f"{month_folder}/performance_data_{start_date.strftime('%Y-%m-%d')}.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'site', 'county', 'rrc_denom', 'rrc_enum', 'erab_denom', 'erab_enum', 'rtp_gap_denom', 'rtp_gap_enum', 'sip_dc_enum', 'sip_dc_denom', 'volte_ia_denom', 'volte_ia_enum', 'dl_user_throughput', 'ul_user_throughput', 'dl_traffic', 'ul_traffic', 'ho_denom', 'ho_enum', 'max_user', 'average_user']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for county, sites in sites_per_county.items():
                for site in sites:
                    for hour in range(24):
                        timestamp = datetime(year, month, day, hour, 0, 0)
                        record = {'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'site': site, 'county': county}
                        # Populate the rest of the fields with random data
                        for field in fieldnames[3:]:
                            record[field] = random.randint(50, 500) if field.endswith('_denom') or field.endswith('_enum') else random.uniform(10.0, 100.0)
                        writer.writerow(record)
        start_date += timedelta(days=1)

# Load existing sites and counties from a sample file
file_path = './data/2024/04/performance_data_2024-04-01.csv'

sites_per_county = load_existing_sites_and_counties(file_path)

# Generate data for the new date range
start_date = datetime(2024, 4, 8)
end_date = datetime(2024, 4, 8)
generate_hourly_data_for_new_range(sites_per_county, start_date, end_date)
