"""Data loading and validation utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import pandas as pd

REQUIRED_COLUMNS = [
    "student_id",
    "department",
    "degree",
    "graduation_year",
    "gpa",
    "company",
    "role",
    "salary_package",
    "offer_type",
    "location",
    "offer_date",
]


@dataclass
class PlacementDataset:
    """Container for placement data and basic metadata."""

    frame: pd.DataFrame
    missing_columns: List[str]

    @property
    def is_valid(self) -> bool:
        return not self.missing_columns



def load_dataset(path: str, required_columns: Iterable[str] = REQUIRED_COLUMNS) -> PlacementDataset:
    """Load the CSV placement dataset and validate column presence."""
    frame = pd.read_csv(path)
    required = list(required_columns)
    missing = [col for col in required if col not in frame.columns]
    return PlacementDataset(frame=frame, missing_columns=missing)



def ensure_valid(dataset: PlacementDataset) -> pd.DataFrame:
    """Raise a descriptive error if the dataset is missing required columns."""
    if dataset.missing_columns:
        missing = ", ".join(dataset.missing_columns)
        raise ValueError(f"Dataset is missing required columns: {missing}")
    return dataset.frame
