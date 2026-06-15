# Backend Architecture

The backend is a Django + Django REST Framework service backed by PostgreSQL.

## App Boundaries

```text
config/
  Django project settings and root URL wiring

hvac/
  Domain app for HVAC predictive health

hvac/models.py
  Database schema and relationships

hvac/scoring.py
  Transparent Day 1 risk scoring logic

hvac/serializers.py
  Request/response shapes and create-time assessment generation

hvac/api/
  API views split by product surface

hvac/urls.py
  Route registration only
```

## API Module Layout

- `hvac/api/vehicles.py`: vehicle CRUD and latest vehicle health.
- `hvac/api/trips.py`: HVAC trip ingestion and assessment creation.
- `hvac/api/reports.py`: dealer report and OEM fleet risk summaries.

`hvac/views.py` is kept only as a compatibility import layer for now. New API
code should go under `hvac/api/`.

## Design Rule

Keep product concepts separate:

- Vehicles are identity and configuration.
- Trip summaries are observed telemetry snapshots.
- Health assessments are predictions derived from telemetry.
- Notifications are delivery decisions for customer, dealer, or OEM audiences.

This keeps the backend ready for future expansion into scheduling, dealer tools,
fleet analytics, and ML model outputs without turning one file into the whole
system.
