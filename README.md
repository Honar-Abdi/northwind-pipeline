# Finland Weather Pipeline

End-to-end data pipeline that ingests Finnish weather observation data
from the Finnish Meteorological Institute (FMI) Open Data API,
transforms it using dbt, and serves analytics-ready data for
energy sector use cases such as consumption forecasting.

## Architecture

`FMI Open Data API → Python (Extract/Load) → PostgreSQL → dbt (Transform) → Power BI`

## Tech Stack

- **Python** — data extraction & loading
- **PostgreSQL** — data warehouse
- **dbt** — SQL transformations, testing & documentation
- **Apache Airflow** — orchestration
- **Azure** — cloud deployment (Blob Storage, Data Factory, Azure PostgreSQL)
- **Power BI** — dashboards & visualization
- **Docker** — containerized development environment

## Status

🚧 Work in progress — currently building local development environment.