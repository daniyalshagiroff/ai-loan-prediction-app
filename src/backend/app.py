from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

model = joblib.load('../models/best_model.joblib')
scaler = joblib.load('../models/scaler.pkl')
feature_names = [
    'no_of_dependents', 'education', 'self_employed', 'income_annum', 
    'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value', 
    'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value', 'Total assets'
]
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    data = pd.DataFrame([data['features']], columns=feature_names)
    print("Input features DataFrame:\n", data.to_string(index=False))

    data[['income_annum', 'loan_amount', 'residential_assets_value', 
        'commercial_assets_value', 'luxury_assets_value', 
        'bank_asset_value', 'Total assets']] = scaler.transform(data[['income_annum', 'loan_amount', 'residential_assets_value', 
        'commercial_assets_value', 'luxury_assets_value', 
        'bank_asset_value', 'Total assets']])
    print("Final features:", data.to_string(index=False))
    prediction = model.predict(data)
    result = int(prediction[0])

    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)