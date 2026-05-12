import pandas as pd
from extract.config import STATIONS
import logging

logger = logging.getLogger(__name__)

# Sarakkeiden uudelleennimeäminen API → tietokanta
COLUMN_MAP = {
    "windspeedms": "wind_speed",
    "precipitation1h": "precipitation",
    "pressure": "air_pressure",
}

EXPECTED_COLS = [
    "station_id", "observed_at", "temperature",
    "wind_speed", "precipitation", "air_pressure", "humidity",
]


def transform_observations(raw: list[dict]) -> pd.DataFrame:
    """Muuntaa raakadatan tietokantaan sopivaan muotoon."""

    df = pd.DataFrame(raw)
    if df.empty:
        return df

    df = df.rename(columns=COLUMN_MAP)
    df["observed_at"] = pd.to_datetime(df["observed_at"], utc=True).dt.tz_localize(None)

    for col in EXPECTED_COLS:
        if col not in df.columns:
            df[col] = None

    return df[EXPECTED_COLS]


def load_stations(engine):
    """Lataa asematiedot kantaan. Ohittaa jo olemassa olevat."""

    rows = [
        {
            "station_id": sid,
            "station_name": info["name"],
            "latitude": info["lat"],
            "longitude": info["lon"],
            "region": info["region"],
        }
        for sid, info in STATIONS.items()
    ]
    df = pd.DataFrame(rows)

    existing = pd.read_sql("SELECT station_id FROM raw.stations", engine)
    new = df[~df["station_id"].isin(existing["station_id"])]

    if not new.empty:
        new.to_sql("stations", engine, schema="raw", if_exists="append", index=False)
        logger.info(f"Lisätty {len(new)} uutta asemaa")
    else:
        logger.info("Kaikki asemat jo kannassa")


def load_observations(df: pd.DataFrame, engine):
    """Lataa havainnot kantaan. Tarkistaa duplikaatit aikaleiman perusteella."""

    if df.empty:
        logger.warning("Ei dataa ladattavaksi")
        return

    latest = pd.read_sql(
        "SELECT station_id, MAX(observed_at) as max_time "
        "FROM raw.weather_observations GROUP BY station_id",
        engine,
    )

    if not latest.empty:
        merged = df.merge(latest, on="station_id", how="left")
        df = merged[
            (merged["max_time"].isna()) | (merged["observed_at"] > merged["max_time"])
        ].drop(columns=["max_time"])

    if df.empty:
        logger.info("Ei uusia havaintoja ladattavaksi")
        return

    df.to_sql(
        "weather_observations", engine, schema="raw", if_exists="append", index=False
    )
    logger.info(f"Ladattu {len(df)} uutta havaintoa")