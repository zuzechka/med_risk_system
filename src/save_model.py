import pandas as pd
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline

import joblib


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dataset.csv"
MODEL_PATH = BASE_DIR / "models" / "gradient_boosting_pipeline.joblib"



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
y = df[TARGETS]


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


model = MultiOutputRegressor(
    GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


print("*" * 60)
print("навчання фынальной")
print("*" * 60)

print(f"\nкількість записів =  {len(X)}")
print(f"кількість ознак =  {len(FEATURES)}")
print(f"кількість цільових показників =  {len(TARGETS)}")

pipeline.fit(X, y)



joblib.dump(pipeline, MODEL_PATH)


print("\n" + "*" * 60)
print("модель збережена")
print("*" * 60)

print(f"\nфайл:")
print(MODEL_PATH)

print("\nмодель має:")
print("передобробку категоріальних ознак")
print("Gradient Boosting")
print("усі 4 цільові показники")