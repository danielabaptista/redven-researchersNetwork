import pandas as pd
import json
import sys
from pathlib import Path
from geopy.geocoders import Nominatim
import pycountry_convert as pc
import time

geolocator = Nominatim(user_agent="geo_lookup")


def get_geo_info(city, country):
    query = f"{city}, {country}" if country else city
    try:
        location = geolocator.geocode(query)
        if location:
            lat, lon = location.latitude, location.longitude
            country_name = location.raw.get("address", {}).get("country")
            return lat, lon
    except Exception as e:
        print(f"⚠️ Error geocoding {query}: {e}")
    return None, None, None

def sheet_to_json(input_file, output_file=None):
    file_path = Path(input_file)
    if not file_path.exists():
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    # Read CSV
    df = pd.read_csv(file_path)

    # Rename columns
    df = df.rename(columns={
        "Nombre y Apellido": "name",
        "Ciudad y País": "city_country",
        "Email": "email",
        "Universidad": "university",
        "Rol": "role"
    })

    # Split city and country for geocoding
    df[["city", "country"]] = df["city_country"].str.split(",", n=1, expand=True)
    df["city"] = df["city"].str.strip()
    df["country"] = df["country"].str.strip().fillna("")

    # Get geolocation
    lats, lons = [], []
    for _, row in df.iterrows():
        lat, lon = get_geo_info(row["city"], row["country"])
        lats.append(lat)
        lons.append(lon)
        time.sleep(1)  # avoid API rate limits

    df["lat"] = lats
    df["lon"] = lons
  

    # Combine city + country for JSON
    df["city"] = df["city"] + (", " + df["country"]).where(df["country"] != "", "")

    # Keep only needed columns
    df = df[["name", "city", "email", "university", "role", "lat", "lon"]]

    # Convert to JSON
    data = df.to_dict(orient="records")

    if output_file is None:
        output_file = file_path.with_suffix(".json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON file created: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file> [output_file]")
        sys.exit(1)
   
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    sheet_to_json(input_file, output_file)

 # to use write in terminal: python dataPrep.py DataRedVen.csv