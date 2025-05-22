import requests

def get_phone_info(phone_number: str) -> str:
    API_KEY = "77a50c5cc4cef4a9c799c140cf210ab6"  # Get it from numverify.com
    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={phone_number}"

    try:
        res = requests.get(url)
        data = res.json()

        if data.get("valid"):
            return (
                f"📱 Phone Number: {data['international_format']}\n"
                f"🌍 Country: {data['country_name']} ({data['country_code']})\n"
                f"📡 Carrier: {data['carrier']}\n"
                f"🧾 Line Type: {data['line_type']}\n"
                f"✅ Valid: Yes"
            )
        else:
            return "❌ Invalid phone number."
    except Exception as e:
        return f"❌ Error: {e}"
