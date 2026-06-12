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
docs/
  day1-design.md
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

## View The Static Product Mockup

Open `prototype/index.html` in a browser.

## Run Tests

```bash
python -m pytest
```
