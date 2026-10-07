const form = document.getElementById("riskForm");
const result = document.getElementById("result");
const submitButton = form.querySelector('button[type="submit"]');
const resetButton = document.getElementById("resetButton");

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const data = {
        age: Number(document.getElementById("age").value),
        sex: document.getElementById("sex").value,
        bmi: Number(document.getElementById("bmi").value),
        glucose_mg_dL: Number(document.getElementById("glucose_mg_dL").value),
        blood_pressure_systolic: Number(
            document.getElementById("blood_pressure_systolic").value
        ),
        cholesterol_mg_dL: Number(
            document.getElementById("cholesterol_mg_dL").value
        ),
        hdl_mg_dL: Number(
            document.getElementById("hdl_mg_dL").value
        ),
        ldl_mg_dL: Number(
            document.getElementById("ldl_mg_dL").value
        ),
        creatinine_mg_dL: Number(
            document.getElementById("creatinine_mg_dL").value
        ),
        hemoglobin_g_dL: Number(
            document.getElementById("hemoglobin_g_dL").value
        ),
        insulin_uU_mL: Number(
            document.getElementById("insulin_uU_mL").value
        ),
        smoking_status: document.getElementById("smoking_status").value,
        alcohol_use: document.getElementById("alcohol_use").value,
        physical_activity: document.getElementById("physical_activity").value,
        family_history_diabetes: Number(
            document.getElementById("family_history_diabetes").value
        ),
        hypertension_binary: Number(
            document.getElementById("hypertension_binary").value
        )
    };

    result.innerHTML = "Расчёт выполняется...";

    submitButton.disabled = true;
    resetButton.disabled = true;

    submitButton.textContent = "Расчёт выполняется...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const prediction = await response.json();

        if (!response.ok) {
            throw new Error(
                prediction.error || "Ошибка при получении прогноза"
            );
        }

        const diabetesRisk = Math.min(
            Math.max(prediction.diabetes_risk * 100, 0),
            100
        );

        const heartRisk = Math.min(
            Math.max(prediction.heart_disease_risk * 100, 0),
            100
        );

        const kidneyRisk = Math.min(
            Math.max(prediction.kidney_disease_risk * 100, 0),
            100
        );

        const strokeRisk = Math.min(
            Math.max(prediction.stroke_risk * 100, 0),
            100
        );

        result.innerHTML = `
            <h2>Результаты оценки риска</h2>

            <div class="results-grid">

                <div class="result-card">
                    <h3>Риск диабета</h3>

                    <div class="result-value">
                        ${diabetesRisk.toFixed(2)}%
                    </div>

                    <div class="risk-bar">
                        <div
                            class="risk-bar-fill"
                            style="width: ${diabetesRisk}%"
                        ></div>
                    </div>
                </div>

                <div class="result-card">
                    <h3>Риск сердечно-сосудистого заболевания</h3>

                    <div class="result-value">
                        ${heartRisk.toFixed(2)}%
                    </div>

                    <div class="risk-bar">
                        <div
                            class="risk-bar-fill"
                            style="width: ${heartRisk}%"
                        ></div>
                    </div>
                </div>

                <div class="result-card">
                    <h3>Риск заболевания почек</h3>

                    <div class="result-value">
                        ${kidneyRisk.toFixed(2)}%
                    </div>

                    <div class="risk-bar">
                        <div
                            class="risk-bar-fill"
                            style="width: ${kidneyRisk}%"
                        ></div>
                    </div>
                </div>

                <div class="result-card">
                    <h3>Риск инсульта</h3>

                    <div class="result-value">
                        ${strokeRisk.toFixed(2)}%
                    </div>

                    <div class="risk-bar">
                        <div
                            class="risk-bar-fill"
                            style="width: ${strokeRisk}%"
                        ></div>
                    </div>
                </div>

            </div>

            <div class="disclaimer">
                Расчёт представляет собой результат работы математической модели
                машинного обучения и носит информационный характер.
                Он не является медицинским диагнозом и не заменяет консультацию
                квалифицированного медицинского специалиста.
            </div>
        `;

    } catch (error) {
        result.innerHTML = `
            <div class="error-message">
                <strong>Не удалось выполнить расчёт.</strong>
                <p>${error.message}</p>
            </div>
        `;

        console.error(error);

    } finally {
        submitButton.disabled = false;
        resetButton.disabled = false;
        submitButton.textContent = "Рассчитать риск";
    }
});

resetButton.addEventListener("click", function() {
    form.reset();
    result.innerHTML = "";
});