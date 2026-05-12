# Northwind Pipeline

Data pipeline that collects Finnish weather observations from the FMI Open Data API, loads them into PostgreSQL, and transforms the data for energy sector analytics.

## Architecture

```
FMI Open Data API -> Python (extract/load) -> PostgreSQL -> dbt -> Power BI
```

## Tech stack

- Python
- PostgreSQL (Docker)
- dbt
- Apache Airflow
- Azure (Blob Storage, Data Factory, Azure PostgreSQL)
- Power BI
- Docker

## Project structure

```
northwind-pipeline/
├── extract/            # FMI API client and configuration
├── load/               # Database connection and data loading
├── sql/                # Database schemas and migrations
├── dbt/                # Transformations (wip)
├── airflow/            # Orchestration DAGs (wip)
├── tests/
├── logs/
├── docker-compose.yml
├── run_pipeline.py
├── requirements.txt
└── .env.example
```

## Getting started

```bash
git clone https://github.com/Honar-Abdi/northwind-pipeline.git
cd northwind-pipeline
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # add your credentials
docker compose up -d
python run_pipeline.py
```

## Data sources

- [FMI Open Data](https://opendata.fmi.fi/) — hourly weather observations from stations across Finland

## Status

Work in progress.
