import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def get_phone_info(phone_number: str) -> str:
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country = geocoder.description_for_number(parsed_number, "en")
        sim_carrier = carrier.name_for_number(parsed_number, "en")
        timezones = timezone.time_zones_for_number(parsed_number)

        return (
            f"📱 Phone Number: {phone_number}\n"
            f"🌍 Country/Region: {country}\n"
            f"📡 Carrier: {sim_carrier}\n"
            f"🕓 Timezone(s): {', '.join(timezones)}"
        )
    except Exception as e:
        return f"❌ Error: {e}"