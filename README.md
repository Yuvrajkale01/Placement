# Placement Intelligence System

This project provides a lightweight, modular system for handling student placement data. It can:

- Predict salary packages from historical placement records.
- Flag suspicious or outlier offers.
- Generate dashboard-ready metrics.
- Auto-write narrative reports for placement cells.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m placement.main --input data/placements.csv --report out/report.md
```

## Modules

- `placement.data`: load and validate placement datasets.
- `placement.model`: train and run salary prediction models.
- `placement.fraud`: detect suspicious offers.
- `placement.dashboard`: build summary metrics for dashboards.
- `placement.report`: generate auto-written reports.

## Sample data

Use a CSV with columns:

- `student_id`
- `department`
- `degree`
- `graduation_year`
- `gpa`
- `company`
- `role`
- `salary_package`
- `offer_type` (on-campus/off-campus)
- `location`
- `offer_date`

