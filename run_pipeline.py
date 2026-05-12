"""Pääskripti: hakee eilisen datan kaikilta asemilta ja lataa kantaan."""

from datetime import datetime, timedelta, timezone
import logging

from extract.config import STATIONS
from extract.fmi_client import fetch_observations
from load.db import engine
from load.loader import load_stations, load_observations, transform_observations

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def main():
    yesterday = datetime.now(tz=timezone.utc) - timedelta(days=1)
    start = yesterday.strftime("%Y-%m-%dT00:00:00Z")
    end = yesterday.strftime("%Y-%m-%dT23:59:00Z")

    logger.info(f"Haetaan data aikavälille {start} — {end}")

    load_stations(engine)

    all_observations = []
    for fmisid, info in STATIONS.items():
        logger.info(f"Haetaan: {info['name']} ({fmisid})")
        try:
            raw = fetch_observations(fmisid, start, end)
            df = transform_observations(raw)
            all_observations.append(df)
            logger.info(f"  -> {len(df)} havaintoa")
        except Exception as e:
            logger.error(f"  → Virhe: {e}")

    if all_observations:
        import pandas as pd
        combined = pd.concat(all_observations, ignore_index=True)
        load_observations(combined, engine)

    logger.info("Pipeline valmis!")


if __name__ == "__main__":
    main()