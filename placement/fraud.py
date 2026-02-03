"""Suspicious offer detection utilities."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class SuspiciousOffer:
    """Represents a suspicious offer and supporting metrics."""

    student_id: str
    company: str
    role: str
    salary_package: float
    z_score: float


def flag_suspicious_offers(
    frame: pd.DataFrame,
    salary_column: str = "salary_package",
    z_threshold: float = 2.5,
) -> pd.DataFrame:
    """Flag suspicious offers using a z-score threshold."""
    output = frame.copy()
    salaries = output[salary_column].astype(float)
    std_dev = salaries.std(ddof=0)
    if std_dev == 0 or np.isnan(std_dev):
        z_scores = pd.Series(0.0, index=salaries.index)
    else:
        z_scores = (salaries - salaries.mean()) / std_dev
    output["salary_z_score"] = z_scores
    output["is_suspicious"] = z_scores.abs() >= z_threshold
    return output


def summarize_suspicious_offers(frame: pd.DataFrame) -> list[SuspiciousOffer]:
    """Create a structured list of suspicious offers for reporting."""
    suspicious = frame[frame["is_suspicious"]].copy()
    summaries: list[SuspiciousOffer] = []
    for _, row in suspicious.iterrows():
        summaries.append(
            SuspiciousOffer(
                student_id=str(row.get("student_id", "")),
                company=str(row.get("company", "")),
                role=str(row.get("role", "")),
                salary_package=float(row.get("salary_package", 0.0)),
                z_score=float(row.get("salary_z_score", np.nan)),
            )
        )
    return summaries
