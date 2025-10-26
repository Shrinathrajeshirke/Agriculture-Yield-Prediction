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

## Route for home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # Get form data with proper type conversion
            data = CustomData(
                Soil_Quality=float(request.form.get('Soil_Quality')),
                Seed_Variety=int(request.form.get('Seed_Variety')),
                Fertilizer_Amount_kg_per_hectare=float(request.form.get('Fertilizer_Amount_kg_per_hectare')),
                Sunny_Days=float(request.form.get('Sunny_Days')),
                Rainfall_mm=float(request.form.get('Rainfall_mm')),
                Irrigation_Schedule=float(request.form.get('Irrigation_Schedule')),
            )

            pred_df = data.get_data_as_data_frame()
            print("Input DataFrame:")
            print(pred_df)
            logging.info(f"Prediction input: {pred_df.to_dict()}")

            print("Before calling predict pipeline")
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)
            print("After calling predict pipeline")
            print(f"Prediction result: {results}")
            
            # Round the result for better display
            final_result = round(results[0], 2)
            logging.info(f"Prediction result: {final_result}")
            
            return render_template('home.html', results=final_result)
            
        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            print(error_message)
            logging.error(error_message)
            return render_template('home.html', results=f"Error: {str(e)}")
        
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080)) 
    app.run(host="0.0.0.0", port=port, debug=True)