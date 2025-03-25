import os
import re
import time
import shutil
import requests
import pandas as pd

# Define download_file
def download_file(url):
    """ Function to download requested LAT data
    """
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename

# Define the base directory
base_dir = "/Volumes/Seagate/RandomPhotonData"
os.makedirs(base_dir, exist_ok=True)

# Load coordinates from file
catalog_file = "random_equatorial_points.csv" 

df = pd.read_csv(catalog_file, usecols=[0, 1], names=["RA", "DEC"], skiprows=1)

# Loop over each coordinate and perform the data query
for idx, row in df.iterrows():
    source_folder = os.path.join(base_dir, f"Source_{idx + 1}")  # Folder for each source
    ra, dec = row["RA"], row["DEC"]

    print(f"\nProcessing Source {idx + 1}: RA={ra}, Dec={dec}")
    os.makedirs(source_folder, exist_ok=True)
    os.chdir(source_folder)

    if os.path.exists("ft1.txt"):
        print("FT1.txt already exists. Skipping download.")
        continue

    # Query parameters for Fermi LAT Data Query
    query_coords = f"{ra:.5f}, {dec:.5f}"
    query_args = {
        "destination": "query",
        "coordfield": query_coords,
        "coordsystem": "J2000",
        "shapefield": "14.1",
        "timefield": "239557417, 738892801",  # Adjust time range if needed
        "timetype": "MET",
        "energyfield": "100, 300000",
        "photonOrExtendedOrNone": "Photon",
        "spacecraft": "off",
    }

    print("Submitting query...")
    query = requests.post("https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi", data=query_args)

    regex_time = re.search(r'The estimated time for your query to complete is ([0-9]*) seconds', query.text)
    regex_link = re.search(r'The results of your query may be found at <a href="(.*)">', query.text)

    if not regex_time or not regex_link:
        print(f"Query failed for Source {idx + 1}. Skipping...")
        continue

    waiting_time = int(regex_time.group(1)) / 4
    print(f"Estimated query time: {regex_time.group(1)} seconds. Checking periodically...")

    for i in range(10):
        time.sleep(waiting_time)
        print("Checking query status...")
        data_links = requests.get(regex_link.group(1))
        if "Query complete" in data_links.text:
            break
        if i == 9:
            print(f"Query for Source {idx + 1} did not complete. Skipping...")
            continue

    print("Downloading data files...")
    regex_latdata = re.findall(r'wget (https.*?fits)', data_links.text)

    if not regex_latdata:
        print(f"No data found for Source {idx + 1}. Skipping...")
        continue

    for filelink in regex_latdata:
        print(f"Downloading {filelink}")
        download_file(filelink)

    # Create a txt file with the list of downloaded FT1 files
    os.system("ls *PH*.fits > ft1.txt")
    print(f"Created ft1.txt for Source {idx + 1}")

print("All sources processed.")