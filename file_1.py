import pandas as pd
from tqdm import tqdm
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import math
import logging

def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Earth radius in km
    return c * r

def process_villages(txt_file, output_csv, log_file='geocode_log.txt'):
    # Set up logging
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

    # Read village names from txt file
    with open(txt_file, 'r') as f:
        villages = [line.strip() for line in f if line.strip()]

    # Initialize geolocator with rate limiter
    geolocator = Nominatim(user_agent="village_locator")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    results = []
    ref_lat, ref_lon = 22.6526, 86.3515  # Reference coordinates

    for village in tqdm(villages, desc="Processing villages"):
        location = geocode(village + ", India")
        if location:
            lat, lon = location.latitude, location.longitude
            dist = haversine(ref_lat, ref_lon, lat, lon)
            logging.info(f"FOUND: {village} -> ({lat}, {lon})")
        else:
            lat, lon, dist = None, None, None
            logging.warning(f"NOT FOUND: {village}")
        results.append({'Village': village, 'Latitude': lat, 'Longitude': lon, 'Distance_km': dist})

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Saved results to {output_csv}")
    print(f"Log written to {log_file}")

# Example usage:
process_villages('villageList.txt', 'villages_with_distance.csv')
