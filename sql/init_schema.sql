-- Skeemat: raw = raakadata API:sta, staging = puhdistettu, marts = analyysivalmis
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;

-- FMI:n mittausasemat
CREATE TABLE raw.stations (
    station_id VARCHAR(20) PRIMARY KEY,
    station_name VARCHAR(200) NOT NULL,
    latitude NUMERIC(8,5),
    longitude NUMERIC(8,5),
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Yksittäiset säähavainnot per asema ja ajanhetki
CREATE TABLE raw.weather_observations (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(20) REFERENCES raw.stations(station_id),
    observed_at TIMESTAMP NOT NULL,
    temperature NUMERIC(5,2),       -- celcius
    wind_speed NUMERIC(5,2),        -- m/s
    precipitation NUMERIC(5,2),     -- mm
    air_pressure NUMERIC(7,2),      -- hPa
    humidity NUMERIC(5,2),          -- %
    cloud_cover INTEGER,            -- oktaavia (0-8)
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nopeutetaan hakuja aseman ja ajan perusteella
CREATE INDEX idx_observations_station_time
    ON raw.weather_observations(station_id, observed_at);