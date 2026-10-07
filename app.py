from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import sys
import os

# Add project root to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.logger import logging

application = Flask(__name__)
app = application

FEATURE_LIMITS = {
    "Soil_Quality": (50, 100),
    "Fertilizer_Amount_kg_per_hectare": (50, 300),
    "Sunny_Days": (50, 150),
    "Rainfall_mm": (100, 900),
    "Irrigation_Schedule": (0, 15),
}
VALID_SEED_VARIETIES = {0, 1}


def validate_inputs(form):
    errors = []
    for name, (lo, hi) in FEATURE_LIMITS.items():
        try:
            value = float(form.get(name))
        except (TypeError, ValueError):
            errors.append(f"{name} must be a number.")
            continue
        if not lo <= value <= hi:
            errors.append(f"{name} must be between {lo} and {hi}.")
        elif name == "Irrigation_Schedule" and value != int(value):
            errors.append("Irrigation_Schedule must be a whole number.")
    try:
        if int(form.get("Seed_Variety")) not in VALID_SEED_VARIETIES:
            errors.append("Seed_Variety must be 0 or 1.")
    except (TypeError, ValueError):
        errors.append("Seed_Variety must be 0 or 1.")
    return errors

## Route for home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html', limits=FEATURE_LIMITS)

    errors = validate_inputs(request.form)
    if errors:
        return render_template('home.html', results="Error: " + " ".join(errors),
                               limits=FEATURE_LIMITS)
    try:
        data = CustomData(
            Soil_Quality=float(request.form['Soil_Quality']),
            Seed_Variety=int(request.form['Seed_Variety']),
            Fertilizer_Amount_kg_per_hectare=float(request.form['Fertilizer_Amount_kg_per_hectare']),
            Sunny_Days=float(request.form['Sunny_Days']),
            Rainfall_mm=float(request.form['Rainfall_mm']),
            Irrigation_Schedule=int(float(request.form['Irrigation_Schedule'])),
        )
        results = PredictPipeline().predict(data.get_data_as_data_frame())
        final_result = round(float(results[0]), 2)
        return render_template('home.html', results=final_result, limits=FEATURE_LIMITS)
    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        return render_template('home.html',
                               results="Error: prediction failed. Please check your inputs.",
                               limits=FEATURE_LIMITS)
        
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080)) 
    app.run(host="0.0.0.0", port=port, debug=False)