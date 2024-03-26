import csv
import os
import random
import gzip
from faker import Faker
from datetime import datetime, timedelta

def generate_hourly_data(sites_per_county, start_year):
    fake = Faker()
    schema = {
        'timestamp': None,
        'site': None,
        'county': None,
        'rrc_denom': 'random_int|100;1000',
        'rrc_enum': 'random_int|0;100',
        'erab_denom': 'random_int|100;1000',
        'erab_enum': 'random_int|0;100',
        'rtp_gap_denom': 'random_int|100;1000',
        'rtp_gap_enum': 'random_int|0;100',
        'sip_dc_enum': 'random_int|0;100',
        'sip_dc_denom': 'random_int|100;1000',
        'volte_ia_denom': 'random_int|100;1000',
        'volte_ia_enum': 'random_int|0;100',
        'dl_user_throughput': 'random_float|0.1;1000.0',
        'ul_user_throughput': 'random_float|0.1;1000.0',
        'dl_traffic': 'random_float|0.1;1000.0',
        'ul_traffic': 'random_float|0.1;1000.0',
        'ho_denom': 'random_int|100;1000',
        'ho_enum': 'random_int|0;100',
        'max_user': 'random_float|0.1;100.0',
        'average_user': 'random_float|0.1;100.0',
    }

    current_timestamp = datetime.now()
    start_date = datetime(start_year, 1, 1, 0, 0, 0)
    end_date = datetime(current_timestamp.year, current_timestamp.month, 1, current_timestamp.hour, 0, 0)

    while start_date < end_date:
        year_month = f"{start_date.year}-{start_date.month:02d}"
        filename = f"data/performance_data_{year_month}.csv.gz"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with gzip.open(filename, 'at') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=schema.keys())
            if os.stat(filename).st_size == 0:
                writer.writeheader()

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
                                    generated_value = random.uniform(*args)
                                else:
                                    generated_value = random.randint(*args)
                            else:
                                generated_value = getattr(fake, method)()
                            record[field] = generated_value
                    writer.writerow(record)
        start_date += timedelta(hours=1)

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

# Generate hourly data until current timestamp from the specified year
start_year = 2022  # Change this to the desired start year
generate_hourly_data(sites_per_county, start_year)
