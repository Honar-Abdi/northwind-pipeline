import requests
from lxml import etree
from extract.config import FMI_BASE_URL, FMI_NAMESPACES, FMI_PARAMETERS, FMI_TIMESTEP
import logging

logger = logging.getLogger(__name__)


def fetch_observations(fmisid: str, start: str, end: str) -> list[dict]:
    """Hakee säähavainnot yhdeltä asemalta annetulta aikaväliltä."""

    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "getFeature",
        "storedquery_id": "fmi::observations::weather::simple",
        "fmisid": fmisid,
        "parameters": FMI_PARAMETERS,
        "timestep": FMI_TIMESTEP,
        "starttime": start,
        "endtime": end,
    }

    response = requests.get(FMI_BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    root = etree.fromstring(response.content)
    members = root.findall(".//BsWfs:BsWfsElement", FMI_NAMESPACES)

    # Yksi XML-elementti = yksi parametri yhdeltä ajanhetkeltä
    # Ryhmitellään aikaleiman perusteella yhdeksi riviksi
    raw_data = {}
    for member in members:
        time_str = member.find("BsWfs:Time", FMI_NAMESPACES).text
        param_name = member.find("BsWfs:ParameterName", FMI_NAMESPACES).text
        param_value = member.find("BsWfs:ParameterValue", FMI_NAMESPACES).text

        if time_str not in raw_data:
            raw_data[time_str] = {"observed_at": time_str, "station_id": fmisid}

        try:
            raw_data[time_str][param_name] = float(param_value)
        except (ValueError, TypeError):
            raw_data[time_str][param_name] = None

    logger.info(f"Haettu {len(raw_data)} havaintoa asemalta {fmisid}")
    return list(raw_data.values())