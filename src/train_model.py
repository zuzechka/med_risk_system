import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


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
y = df[TARGETS]

NUMERIC_FEATURES = [
    "age",
    "bmi",
    "glucose_mg_dL",
    "blood_pressure_systolic",
    "cholesterol_mg_dL",
    "hdl_mg_dL",
    "ldl_mg_dL",
    "creatinine_mg_dL",
    "hemoglobin_g_dL",
    "insulin_uU_mL",
    "family_history_diabetes",
    "hypertension_binary"
]

CATEGORICAL_FEATURES = [
    "sex",
    "smoking_status",
    "alcohol_use",
    "physical_activity"
]


#розділення на тестові та тренувальні дані

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

#передооброка категоріальних даних

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

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

models = {

    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": MultiOutputRegressor(
        GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=3,
            random_state=42
        )
    )
}



#навчання та оцінка моделей
results = []


for model_name, model in models.items():

    print("\n" + "*" * 60)
    print(f"навчання = {model_name}")
    print("*" * 60)

    #навчання
    model.fit(X_train_processed, y_train)

    #передбачення
    y_pred = model.predict(X_test_processed)

    #метрики пок ожного ризику
    print("\nрезультати по кожному ризику =")

    for i, target in enumerate(TARGETS):

        mae = mean_absolute_error(
            y_test.iloc[:, i],
            y_pred[:, i]
        )

        mse = mean_squared_error(
            y_test.iloc[:, i],
            y_pred[:, i]
        )

        rmse = mse ** 0.5

        r2 = r2_score(
            y_test.iloc[:, i],
            y_pred[:, i]
        )

        print(f"\n{target}")
        print(f"  MAE :  {mae:.4f}")
        print(f"  MSE :  {mse:.4f}")
        print(f"  RMSE:  {rmse:.4f}")
        print(f"  R2  :  {r2:.4f}")

        results.append({
            "Model": model_name,
            "Target": target,
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2
        })


results_df = pd.DataFrame(results)


print("\n\n" + "*" * 80)
print("результат порівнння моделей")
print("*" * 80)

print(
    results_df.to_string(
        index=False,
        formatters={
            "MAE": "{:.4f}".format,
            "MSE": "{:.4f}".format,
            "RMSE": "{:.4f}".format,
            "R2": "{:.4f}".format
        }
    )
)



summary = (
    results_df
    .groupby("Model")[["MAE", "MSE", "RMSE", "R2"]]
    .mean()
    .sort_values("RMSE")
)


print("\n\n" + "*" * 80)
print("середні результати моделей")
print("*" * 80)

print(
    summary.to_string(
        formatters={
            "MAE": "{:.4f}".format,
            "MSE": "{:.4f}".format,
            "RMSE": "{:.4f}".format,
            "R2": "{:.4f}".format
        }
    )
)