import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import KFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dataset.csv"

df = pd.read_csv(DATA_PATH)

FEATURES = [
    "age",
    "sex",
    "bmi",
    "glucose_mg_dL",
    "blood_pressure_systolic",
    "cholesterol_mg_dL",
    "hdl_mg_dL",
    "ldl_mg_dL",
    "creatinine_mg_dL",
    "hemoglobin_g_dL",
    "insulin_uU_mL",
    "smoking_status",
    "alcohol_use",
    "physical_activity",
    "family_history_diabetes",
    "hypertension_binary"
]


TARGETS = [
    "diabetes_risk_prob",
    "heart_disease_risk_prob",
    "kidney_disease_risk_prob",
    "stroke_risk_prob"
]


X = df[FEATURES]


CATEGORICAL_FEATURES = [
    "sex",
    "smoking_status",
    "alcohol_use",
    "physical_activity"
]



preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            CATEGORICAL_FEATURES
        )
    ],
    remainder="passthrough"
)


#gradient Boosting

model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)


#Pipeline

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


#крос-валідація
cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


print("*" * 70)
print("5-FOLD CROSS-VALIDATION: GRADIENT BOOSTING")
print("*" * 70)


for target in TARGETS:

    y = df[target]

    scores = cross_val_score(
        pipeline,
        X,
        y,
        cv=cv,
        scoring="r2"
    )

    print("\n" + "*" * 70)
    print(f"цілоьова змінна: {target}")
    print("*" * 70)

    for i, score in enumerate(scores, start=1):
        print(f"Fold {i}: R2 = {score:.4f}")

    print(f"\nсереднє R2: {scores.mean():.4f}")
    print(f"стандартне відхиленнря: {scores.std():.4f}")

    print(
        f"діапазон R2: "
        f"{scores.min():.4f} - {scores.max():.4f}"
    )


print("\n" + "*" * 70)
print("крос-валідація завершена")
print("*" * 70)