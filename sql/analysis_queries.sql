-- Säähavaintojen analyysit
-- Käytetään datan validointiin ja exploratory-analyysiin ennen dbt-mallien rakentamista

-- Havaintojen yleiskatsaus per asema
SELECT
    s.station_name,
    s.region,
    o.observed_at,
    o.temperature,
    o.wind_speed
FROM raw.weather_observations o
JOIN raw.stations s ON o.station_id = s.station_id
ORDER BY o.observed_at
LIMIT 10;

-- Päivätason aggregaatit per asema
SELECT
    s.station_name,
    DATE(o.observed_at) AS day,
    ROUND(AVG(o.temperature), 1) AS avg_temp,
    ROUND(MAX(o.temperature), 1) AS max_temp,
    ROUND(MIN(o.temperature), 1) AS min_temp,
    ROUND(SUM(o.precipitation), 1) AS total_rain_mm
FROM raw.weather_observations o
JOIN raw.stations s ON o.station_id = s.station_id
GROUP BY s.station_name, DATE(o.observed_at)
ORDER BY day, s.station_name;

-- Sadepäivät (yli 1mm vuorokaudessa)
SELECT
    s.station_name,
    DATE(o.observed_at) AS day,
    ROUND(SUM(o.precipitation), 1) AS total_rain_mm
FROM raw.weather_observations o
JOIN raw.stations s ON o.station_id = s.station_id
GROUP BY s.station_name, DATE(o.observed_at)
HAVING SUM(o.precipitation) > 1
ORDER BY total_rain_mm DESC;

-- Lämpötilan muutos peräkkäisten havaintojen välillä
SELECT
    s.station_name,
    o.observed_at,
    o.temperature,
    LAG(o.temperature) OVER (
        PARTITION BY o.station_id
        ORDER BY o.observed_at
    ) AS prev_temp,
    ROUND(
        o.temperature - LAG(o.temperature) OVER (
            PARTITION BY o.station_id
            ORDER BY o.observed_at
        ), 1
    ) AS temp_change
FROM raw.weather_observations o
JOIN raw.stations s ON o.station_id = s.station_id
ORDER BY s.station_name, o.observed_at;

-- Kylmimmät havainnot per alue (top 3)
SELECT * FROM (
    SELECT
        s.region,
        s.station_name,
        o.observed_at,
        o.temperature,
        RANK() OVER (
            PARTITION BY s.region
            ORDER BY o.temperature ASC
        ) AS cold_rank
    FROM raw.weather_observations o
    JOIN raw.stations s ON o.station_id = s.station_id
) ranked
WHERE cold_rank <= 3
ORDER BY region, cold_rank;