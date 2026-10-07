from flask import Flask, request, jsonify, render_template
from pathlib import Path
import joblib
import pandas as pd
import math

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "gradient_boosting_pipeline.joblib"

#завантаження навченої моделі
model = joblib.load(MODEL_PATH)

#перелік ознак, які використовуються моделлю
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

#допустимі значення категоріальних ознак
CATEGORICAL_VALUES = {
    "sex": {"F", "M"},
    "smoking_status": {"never", "former", "current"},
    "alcohol_use": {"no", "occasional", "regular"},
    "physical_activity": {"low", "medium", "high"}
}

#допустимі діапазони числових ознак
NUMERIC_RANGES = {
    "age": (18, 90),
    "bmi": (15, 46.8),
    "glucose_mg_dL": (40, 267),
    "blood_pressure_systolic": (82.3, 177.3),
    "cholesterol_mg_dL": (100, 355.6),
    "hdl_mg_dL": (20, 88.8),
    "ldl_mg_dL": (50, 233.6),
    "creatinine_mg_dL": (0.4, 2.24),
    "hemoglobin_g_dL": (7, 19),
    "insulin_uU_mL": (2, 282.6)
}

#бінарні ознаки, які можуть мати значення 0 або 1
BINARY_FEATURES = {
    "family_history_diabetes",
    "hypertension_binary"
}


@app.route("/")
def home():
    #відображення головної сторінки вебзастосунку
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    #отримання даних, надісланих із вебформи
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Дані не отримано"
        }), 400

    #перевірка наявності всіх обов'язкових полів
    missing_features = [
        feature for feature in FEATURES
        if feature not in data
    ]

    if missing_features:
        return jsonify({
            "error": "Відсутні обов'язкові поля",
            "missing": missing_features
        }), 400

    #перевірка допустимих значень категоріальних ознак
    for feature, allowed_values in CATEGORICAL_VALUES.items():
        if data[feature] not in allowed_values:
            return jsonify({
                "error": f"Недопустиме значення поля: {feature}"
            }), 400

    #перевірка бінарних ознак
    for feature in BINARY_FEATURES:
        if data[feature] not in (0, 1):
            return jsonify({
                "error": f"Поле {feature} повинно мати значення 0 або 1"
            }), 400

    input_data = {}

    #перевірка числових значень та їхніх допустимих діапазонів
    for feature, (minimum, maximum) in NUMERIC_RANGES.items():

        try:
            value = float(data[feature])

            if not math.isfinite(value):
                raise ValueError

        except (TypeError, ValueError):
            return jsonify({
                "error": f"Некоректне числове значення поля: {feature}"
            }), 400

        if value < minimum or value > maximum:
            return jsonify({
                "error": (
                    f"Значення поля {feature} повинно знаходитися "
                    f"в діапазоні від {minimum} до {maximum}"
                )
            }), 400

        input_data[feature] = value

    #додавання категоріальних та бінарних ознак до вхідних даних
    input_data["sex"] = data["sex"]
    input_data["smoking_status"] = data["smoking_status"]
    input_data["alcohol_use"] = data["alcohol_use"]
    input_data["physical_activity"] = data["physical_activity"]
    input_data["family_history_diabetes"] = data["family_history_diabetes"]
    input_data["hypertension_binary"] = data["hypertension_binary"]

    #формування таблиці з вхідними даними для моделі
    input_df = pd.DataFrame([input_data])

    try:
        #отримання прогнозу за допомогою навченої моделі
        prediction = model.predict(input_df)[0]

    except Exception:
        return jsonify({
            "error": "Не вдалося виконати розрахунок"
        }), 500

    #обмеження прогнозованих значень діапазоном від 0 до 1
    prediction = [
        min(max(float(value), 0.0), 1.0)
        for value in prediction
    ]

    #формування результату прогнозування
    result = {
        "diabetes_risk": round(prediction[0], 4),
        "heart_disease_risk": round(prediction[1], 4),
        "kidney_disease_risk": round(prediction[2], 4),
        "stroke_risk": round(prediction[3], 4)
    }

    return jsonify(result)


if __name__ == "__main__":
    #запуск Flask-застосунку в режимі налагодження
    app.run(debug=True)