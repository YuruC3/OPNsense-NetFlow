import IP2Location
from typing import Optional, Annotated

# Load database once
ip2loc_db = IP2Location.IP2Location("IP2LOCATION-LITE-DB9.BIN")

def ermWhatTheCountry(inpIpAddress: Annotated[str, "Some IP address that ya want to get country for"]):
    try:
        skibidi = ip2loc_db.get_all(inpIpAddress)

        #return rec.country_long  # Full country name, e.g. "Sweden"
        return skibidi.country_short

    except Exception as errrrrr:
        return f"Error: {errrrrr}"

#print(ermWhatTheCountry("65.109.142.32"))

