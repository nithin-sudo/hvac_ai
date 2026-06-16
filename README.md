# HVAC AI Predictive Health Platform

This repository starts the HVAC-first version of an AI-powered vehicle health
platform.

The first product goal is simple: detect early HVAC degradation from lightweight
vehicle telemetry, create a health/risk score, and route the result to the right
experience for the customer, dealer, and OEM quality team.

## Day 1 Scope

- Define the HVAC-first product shape.
- Model a lightweight HVAC trip summary.
- Score HVAC health with transparent rules before using ML.
- Produce a simple customer alert and dealer/OEM diagnostic outline.

This is not the final production architecture. It is a small, testable starting
point for product and engineering discussion.

## Project Layout

```text
config/
  settings.py
  urls.py
docs/
  backend-architecture.md
  day1-design.md
hvac/
  api/
  models.py
  scoring.py
  serializers.py
  services/
  views.py
prototype/
  index.html
  styles.css
src/
  hvac_ai/
    cli.py
    models.py
    sample_data.py
    scoring.py
tests/
  test_scoring.py
```

## Run The Demo

```bash
python -m hvac_ai.cli
```

## Backend Setup

Create a `.env` file from `.env.example`, then set PostgreSQL connection values:

```bash
copy .env.example .env
```

Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run Django checks:

```bash
.venv\Scripts\python.exe manage.py check
```

After PostgreSQL is running and the database exists:

```bash
.venv\Scripts\python.exe manage.py migrate
```

Seed demo HVAC records:

```bash
.venv\Scripts\python.exe manage.py seed_hvac_demo
```

Start the backend:

```bash
.venv\Scripts\python.exe manage.py runserver
```

First API shape:

```text
POST /api/vehicles/
POST /api/hvac/trips/
GET  /api/vehicles/<vin>/health/
GET  /api/vehicles/<vin>/dealer-report/
GET  /api/fleet/hvac-risk/
GET  /api/notifications/?vin=<vin>&pending=true
```

## View The Static Product Mockup

Open `prototype/index.html` in a browser.

## Run Tests

```bash
python -m unittest discover -s tests
```
