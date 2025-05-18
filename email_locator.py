import requests
import re

def extract_sender_ip(email_header: str) -> str | None:
    ip_pattern = r'\[?(\d{1,3}(?:\.\d{1,3}){3})\]?'
    match = re.search(ip_pattern, email_header)
    return match.group(1) if match else None

def get_email_location(ip_address: str) -> str:
    try:
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url)
        data = response.json()

        country = data.get("country", "Unknown")
        region = data.get("region", "Unknown")
        city = data.get("city", "Unknown")
        location = data.get("loc", "Unknown")

        return (
            f"🌍 Email Location: {city}, {region}, {country}\n"
            f"🗺️ Coordinates: {location}"
        )
    except Exception as e:
        return f"❌ Error locating email IP: {e}"