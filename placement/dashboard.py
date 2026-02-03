"""Dashboard metric generation."""
from __future__ import annotations

import pandas as pd


def build_dashboard_metrics(frame: pd.DataFrame) -> dict[str, object]:
    """Generate summary metrics for dashboards."""
    metrics = {
        "total_students": int(frame["student_id"].nunique()),
        "total_offers": int(frame.shape[0]),
        "median_salary": float(frame["salary_package"].median()),
        "average_salary": float(frame["salary_package"].mean()),
        "top_departments": (
            frame.groupby("department")["salary_package"]
            .median()
            .sort_values(ascending=False)
            .head(5)
            .to_dict()
        ),
        "offers_by_company": (
            frame["company"].value_counts().head(10).to_dict()
        ),
    }
    return metrics
