import csv
import os
import random
from faker import Faker
from datetime import datetime, timedelta

def generate_hourly_data_for_years(sites_per_county, num_years=3):
    fake = Faker()
    schema = {
        'timestamp': None,
        'site': None,
        'county': None,
        'rrc_denom': 'random_int|50;500',  # Adjusted range for morning hours
        'rrc_enum': 'random_int|0;50',     # Adjusted range for morning hours
        'erab_denom': 'random_int|50;500', # Adjusted range for morning hours
        'erab_enum': 'random_int|0;50',    # Adjusted range for morning hours
        'rtp_gap_denom': 'random_int|50;500', # Adjusted range for morning hours
        'rtp_gap_enum': 'random_int|0;50',    # Adjusted range for morning hours
        'sip_dc_enum': 'random_int|0;50',      # Adjusted range for morning hours
        'sip_dc_denom': 'random_int|50;500',   # Adjusted range for morning hours
        'volte_ia_denom': 'random_int|50;500', # Adjusted range for morning hours
        'volte_ia_enum': 'random_int|0;50',    # Adjusted range for morning hours
        'dl_user_throughput': 'random_float|10.0;100.0',  # Adjusted range for morning hours
        'ul_user_throughput': 'random_float|10.0;100.0',  # Adjusted range for morning hours
        'dl_traffic': 'random_float|10.0;100.0',           # Adjusted range for morning hours
        'ul_traffic': 'random_float|10.0;100.0',           # Adjusted range for morning hours
        'ho_denom': 'random_int|50;500',     # Adjusted range for morning hours
        'ho_enum': 'random_int|0;50',        # Adjusted range for morning hours
        'max_user': 'random_float|50.0;200.0', # Adjusted range for normal hours
        'average_user': 'random_float|20.0;150.0', # Adjusted range for normal hours
    }

    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=num_years * 365)

    while start_date <= end_date:
        year_month = start_date.strftime('%Y_%m')
        filename = f"data/performance_data_{year_month}.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema.keys())
            writer.writeheader()

            # Find the first day of the month
            first_day_of_month = datetime(start_date.year, start_date.month, 1)

            while start_date.month == end_date.month:
                for county, sites in sites_per_county.items():
                    for site in sites:
                        record = {
                            'timestamp': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'site': site,
                            'county': county
                        }
                        for field, generator in schema.items():
                            if generator:
                                method, *args = generator.split('|')
                                if args:
                                    args = [float(arg) if '.' in arg else int(arg) for arg in args[0].split(';')]
                                    if method == 'random_float':
                                        if 6 < start_date.hour < 23:  # Normal hours
                                            args = [arg * 1.5 for arg in args]  # Increase values for normal hours
                                        elif start_date.hour < 6:  # Early morning hours
                                            args = [arg * 0.5 for arg in args]  # Decrease values for early morning hours
                                        generated_value = random.uniform(*args)
                                    else:
                                        if 6 < start_date.hour < 23:  # Normal hours
                                            args = [int(arg * 1.5) for arg in args]  # Increase values for normal hours
                                        elif start_date.hour < 6:  # Early morning hours
                                            args = [int(arg * 0.5) for arg in args]  # Decrease values for early morning hours
                                        generated_value = random.randint(*args)
                                else:
                                    generated_value = getattr(fake, method)()
                                record[field] = generated_value
                        writer.writerow(record)
                start_date += timedelta(hours=1)
            start_date = first_day_of_month + timedelta(days=1)  # Move to the next month

def generate_site_county_data(num_sites, num_counties):
    fake = Faker()
    site_names = [fake.street_name() for _ in range(num_sites)]
    county_names = [fake.state() for _ in range(num_counties)]

    # Map sites to counties
    sites_per_county = {}
    for site, county in zip(site_names, random.choices(county_names, k=len(site_names))):
        sites_per_county.setdefault(county, []).append(site)

    return sites_per_county

# Specify the number of sites and counties
num_sites = 250
num_counties = 50

# Generate site-county mapping
sites_per_county = generate_site_county_data(num_sites, num_counties)

# Generate hourly data for the last three years, saving separate CSV files for each month
generate_hourly_data_for_years(sites_per_county)
