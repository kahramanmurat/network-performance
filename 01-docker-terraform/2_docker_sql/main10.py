import csv
import os
import random
from faker import Faker
from datetime import datetime, timedelta

def load_sites_from_csv(file_path):
    sites_per_county = {}
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            county = row['county']
            site = row['site']
            if county in sites_per_county:
                if site not in sites_per_county[county]:
                    sites_per_county[county].append(site)
            else:
                sites_per_county[county] = [site]
    return sites_per_county

def generate_hourly_data(sites_per_county):
    fake = Faker()
    schema = {
        'timestamp': None,
        'site': None,
        'county': None,
        'rrc_denom': 'random_int|50;500',
        'rrc_enum': 'random_int|0;50',
        'erab_denom': 'random_int|50;500',
        'erab_enum': 'random_int|0;50',
        'rtp_gap_denom': 'random_int|50;500',
        'rtp_gap_enum': 'random_int|0;50',
        'sip_dc_enum': 'random_int|0;50',
        'sip_dc_denom': 'random_int|50;500',
        'volte_ia_denom': 'random_int|50;500',
        'volte_ia_enum': 'random_int|0;50',
        'dl_user_throughput': 'random_float|10.0;100.0',
        'ul_user_throughput': 'random_float|10.0;100.0',
        'dl_traffic': 'random_float|10.0;100.0',
        'ul_traffic': 'random_float|10.0;100.0',
        'ho_denom': 'random_int|50;500',
        'ho_enum': 'random_int|0;50',
        'max_user': 'random_float|50.0;200.0',
        'average_user': 'random_float|20.0;150.0',
    }

    start_date = datetime(2024, 4, 9, 0, 0, 0)  # Start date: Adjust as needed
    end_date = datetime(2024, 4, 9, 23, 0, 0)   # End date: Adjust as needed

    while start_date <= end_date:
        year_month_day = start_date.strftime('%Y-%m-%d')
        filename = f"data/performance_data_{year_month_day}.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema.keys())
            writer.writeheader()

            for county, sites in sites_per_county.items():
                for site in sites:
                    current_hour = 0
                    while current_hour <= 23:
                        record = {
                            'timestamp': start_date.replace(hour=current_hour).strftime('%Y-%m-%d %H:%M:%S'),
                            'site': site,
                            'county': county
                        }
                        for field, generator in schema.items():
                            if generator:
                                method, *args = generator.split('|')
                                if args:
                                    args = [float(arg) if '.' in arg else int(arg) for arg in args[0].split(';')]
                                    if method == 'random_float':
                                        if 6 < current_hour < 23:
                                            args = [arg * 1.5 for arg in args]
                                        elif current_hour < 6:
                                            args = [arg * 0.5 for arg in args]
                                        generated_value = random.uniform(*args)
                                    else:
                                        if 6 < current_hour < 23:
                                            args = [int(arg * 1.5) for arg in args]
                                        elif current_hour < 6:
                                            args = [int(arg * 0.5) for arg in args]
                                        generated_value = random.randint(*args)
                                else:
                                    generated_value = getattr(fake, method)()
                                record[field] = generated_value
                        writer.writerow(record)
                        current_hour += 1
            start_date += timedelta(days=1)

# Specify the path to your existing CSV file
file_path = './data/2024/04/performance_data_2024-04-01.csv'  # Make sure to replace this path with the actual path to your April 1, 2024, CSV file

# Load the existing site and county data
sites_per_county = load_sites_from_csv(file_path)

# Generate hourly data for the specified date range using the same sites and counties
generate_hourly_data(sites_per_county)
