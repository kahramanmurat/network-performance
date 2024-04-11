import requests
from datetime import datetime, timedelta

# Calculate yesterday's date
yesterday = datetime.now() - timedelta(1)
formatted_date = yesterday.strftime('%Y-%m-%d')
year, month, day = formatted_date.split('-')

# GitHub repository details
user_or_org = "kahramanmurat"
repo_name = "network-performance-data"
path = f"{year}/{month}"

# GitHub API URL for contents of the directory
url = f"https://api.github.com/repos/{user_or_org}/{repo_name}/contents/{path}"

response = requests.get(url)
if response.status_code == 200:
    files = response.json()
else:
    print(f"Failed to retrieve directory contents: {response.status_code} - {response.text}")
    files = []

download_url = ""
# Check for the expected file name
expected_file_name = f"performance_data_{formatted_date}.csv"

# Logic to check if the file exists and download it
for file in files:
    if file['name'] == expected_file_name:
        download_url = file['download_url']
        break

if download_url:
    # Perform the download
    response = requests.get(download_url)
    if response.status_code == 200:
        # Save the file locally
        with open(expected_file_name, 'wb') as f:
            f.write(response.content)
        print(f"File {expected_file_name} downloaded successfully.")
    else:
        print(f"Failed to download the file: {response.status_code}")
else:
    print(f"File {expected_file_name} not found.")
