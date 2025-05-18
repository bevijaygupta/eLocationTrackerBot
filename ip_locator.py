import geoip2.database
import os

def get_ip_location(ip_address: str) -> str:
    # Use absolute path to the .mmdb file
    db_path = os.path.join(os.path.dirname(__file__), "Data", "GeoLite2-City.mmdb")

    try:
        reader = geoip2.database.Reader(db_path)
        response = reader.city(ip_address)

        result = (
            f"✅ IP Address: {ip_address}\n"
            f"📍 City: {response.city.name or 'N/A'}\n"
            f"🌍 Country: {response.country.name or 'N/A'}\n"
            f"📌 Latitude: {response.location.latitude}\n"
            f"📌 Longitude: {response.location.longitude}"
        )
        reader.close()
        return result

    except Exception as e:
        return f"❌ Error: {e}"