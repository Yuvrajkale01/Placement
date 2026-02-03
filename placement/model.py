"""Salary prediction model utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURE_COLUMNS = [
    "department",
    "degree",
    "graduation_year",
    "gpa",
    "company",
    "role",
    "offer_type",
    "location",
]
TARGET_COLUMN = "salary_package"


@dataclass
class SalaryModel:
    """A trained salary model and its feature set."""

    pipeline: Pipeline
    features: List[str]

    def predict(self, frame: pd.DataFrame) -> np.ndarray:
        return self.pipeline.predict(frame[self.features])



def train_model(frame: pd.DataFrame) -> SalaryModel:
    """Train a salary prediction model using ridge regression."""
    numeric_features = ["graduation_year", "gpa"]
    categorical_features = [
        col for col in FEATURE_COLUMNS if col not in numeric_features
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
            ("numeric", "passthrough", numeric_features),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("regressor", Ridge(alpha=1.0)),
        ]
    )

    X = frame[FEATURE_COLUMNS]
    y = frame[TARGET_COLUMN]
    pipeline.fit(X, y)

    return SalaryModel(pipeline=pipeline, features=FEATURE_COLUMNS)



def add_predictions(frame: pd.DataFrame, model: SalaryModel) -> pd.DataFrame:
    """Return a copy of the dataset with predicted salary packages."""
    output = frame.copy()
    output["predicted_salary"] = model.predict(output)
    return output
