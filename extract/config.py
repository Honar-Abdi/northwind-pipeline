import os
from dotenv import load_dotenv

load_dotenv()

# Tietokanta
DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# FMI API
FMI_BASE_URL = os.getenv("FMI_BASE_URL")
FMI_NAMESPACES = {
    "wfs": "http://www.opengis.net/wfs/2.0",
    "BsWfs": "http://xml.fmi.fi/schema/wfs/2.0",
    "gml": "http://www.opengis.net/gml/3.2"
}

# Asemat joiden dataa haetaan
STATIONS = {
    "101004": {"name": "Helsinki Kaisaniemi", "lat": 60.17523, "lon": 24.94459, "region": "Uusimaa"},
    "101007": {"name": "Helsinki-Vantaa lentoasema", "lat": 60.32670, "lon": 24.95675, "region": "Uusimaa"},
    "101799": {"name": "Tampere Härmälä", "lat": 61.47842, "lon": 23.75200, "region": "Pirkanmaa"},
    "102035": {"name": "Oulu Pellonpää", "lat": 64.93717, "lon": 25.39078, "region": "Pohjois-Pohjanmaa"},
}

# API-parametrit
FMI_PARAMETERS = "temperature,windspeedms,precipitation1h,pressure,humidity"
FMI_TIMESTEP = "60"