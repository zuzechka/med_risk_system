const form = document.getElementById("riskForm");
const result = document.getElementById("result");
const resetButton = document.getElementById("resetButton");

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const submitButton = form.querySelector('button[type="submit"]');

    //отримання даних з форми
    const data = {
        age: Number(document.getElementById("age").value),
        sex: document.getElementById("sex").value,
        bmi: Number(document.getElementById("bmi").value),
        glucose_mg_dL: Number(
            document.getElementById("glucose_mg_dL").value
        ),
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

    result.innerHTML = `
        <div class="loading-message">
            Виконується розрахунок...
        </div>
    `;

    submitButton.disabled = true;
    submitButton.textContent = "Розрахунок виконується...";

    try {

        //відправлення даних на сервер для отримання прогнозу
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
                prediction.error || "Не вдалося виконати розрахунок"
            );
        }

        //перетворення отриманих значень ризику у відсотки
        const diabetesPercent = Math.min(
            Math.max(prediction.diabetes_risk * 100, 0),
            100
        );

        const heartPercent = Math.min(
            Math.max(prediction.heart_disease_risk * 100, 0),
            100
        );

        const kidneyPercent = Math.min(
            Math.max(prediction.kidney_disease_risk * 100, 0),
            100
        );

        const strokePercent = Math.min(
            Math.max(prediction.stroke_risk * 100, 0),
            100
        );

        //формування та відображення результатів прогнозування
        result.innerHTML = `
            <div class="results-header">
                <h2>Результати оцінки ризику</h2>

                <p>
                    Розрахункові значення, отримані з використанням
                    моделі машинного навчання.
                </p>
            </div>

            <div class="results-grid">

                <div class="result-card">
                    <h3>Ризик діабету</h3>

                    <div class="result-value">
                        ${diabetesPercent.toFixed(2)}%
                    </div>

                    <p class="result-description">
                        Розрахункове значення моделі.
                    </p>

                    <div class="risk-bar">
                        <div
                            class="risk-bar-fill"
                            style="width: ${diabetesPercent}%"
                        ></div>
                    </div>
                </div>

                <div class="result-card">
                    <h3>Ризик серцево-судинного захворювання</h3>

                    <div class="result-value">
                        ${heartPercent.toFixed(2)}%
                    </div>

                    <p class="result-description">
                        Розрахункове значення моделі.
                    </p>

                    <div class="risk-bar">
                        <div
                            class="risk-bar-fill"
                            style="width: ${heartPercent}%"
                        ></div>
                    </div>
                </div>

                <div class="result-card">
                    <h3>Ризик захворювання нирок</h3>

                    <div class="result-value">
                        ${kidneyPercent.toFixed(2)}%
                    </div>

                    <p class="result-description">
                        Розрахункове значення моделі.
                    </p>

                    <div class="risk-bar">
                        <div
                            class="risk-bar-fill"
                            style="width: ${kidneyPercent}%"
                        ></div>
                    </div>
                </div>

                <div class="result-card">
                    <h3>Ризик інсульту</h3>

                    <div class="result-value">
                        ${strokePercent.toFixed(2)}%
                    </div>

                    <p class="result-description">
                        Розрахункове значення моделі.
                    </p>

                    <div class="risk-bar">
                        <div
                            class="risk-bar-fill"
                            style="width: ${strokePercent}%"
                        ></div>
                    </div>
                </div>

            </div>

            <div class="recommendations">
                <h2>Інформаційні рекомендації</h2>

                <ul>
                    <li>
                        Результати оцінки слід розглядати у сукупності
                        з іншими показниками стану здоров'я.
                    </li>

                    <li>
                        Для отримання професійної оцінки стану
                        здоров'я рекомендується звернутися до медичного
                        спеціаліста.
                    </li>

                    <li>
                        При зміні початкових медичних показників
                        рекомендується повторити розрахунок.
                    </li>

                    <li>
                        Отримані значення є результатом роботи
                        математичної моделі та не є медичним
                        діагнозом.
                    </li>
                </ul>
            </div>

            <div class="disclaimer">
                Розрахунок є результатом роботи математичної моделі
                машинного навчання та має інформаційний характер.
                Він не є медичним діагнозом і не замінює консультацію
                кваліфікованого медичного спеціаліста.
            </div>
        `;

    } catch (error) {

        result.innerHTML = `
            <div class="error-message">
                <strong>Помилка:</strong> ${error.message}
            </div>
        `;

        console.error(error);

    } finally {

        submitButton.disabled = false;
        submitButton.textContent = "Розрахувати ризик";
    }
});


resetButton.addEventListener("click", function() {
    //очищення форми та результатів розрахунку
    form.reset();
    result.innerHTML = "";
});

