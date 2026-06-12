# Day 1 Design: HVAC First

## Product Intent

Start with HVAC because customers feel climate performance immediately, the
vehicle already has useful signals, and degradation can appear before a complete
failure.

The first version should prove the loop:

1. Capture lightweight HVAC trip summaries.
2. Compare behavior against expected healthy behavior.
3. Score risk and confidence.
4. Show a simple customer message.
5. Prepare dealer and OEM evidence.

## Minimal Inputs

- Vehicle ID
- Trip timestamp
- Region
- Ambient temperature
- Cabin start temperature
- Target temperature
- Minimum vent temperature
- Time to target
- Average compressor duty
- Refrigerant pressure stability
- Fault code count
- HVAC software version

## Minimal Output

- HVAC health score from 0 to 100
- Risk level: low, medium, high
- Likely issue category
- Confidence
- Recommended action
- Plain-language customer message
- Dealer diagnostic summary

## Day 1 Non-Goals

- No production cloud architecture yet.
- No real ML model yet.
- No connected vehicle ingestion yet.
- No customer-facing mobile or HMI frontend yet.
- No dealer management system integration yet.

## First Architecture Shape

```text
HVAC trip summary
        |
        v
Rule-based scoring engine
        |
        +--> Customer alert
        +--> Dealer pre-diagnosis
        +--> OEM fleet quality signal
```

## Design Principle

Simulate the product truthfully before building the full platform. Rules and
sample data are acceptable for Day 1 if the interfaces reflect what the future
AI system will eventually produce.
