from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import pickle

model = joblib.load('../models/best_model.joblib')
scaler = joblib.load('../models/scaler.pkl')
mean_and_frequent_values = pickle.load(open('../../data/mean_and_frequent_values.pkl', 'rb'))
mean_values = mean_and_frequent_values['mean_values']
most_frequent_values = mean_and_frequent_values['most_frequent_values']
app = Flask(__name__)
REQUIRED_FIELDS = ['cibil_score', 'loan_term']

@app.route('/predict', methods=['POST'])
def predict():
    print("NEW NEW NEW NEW NEW NEW NEW NEW NEW NEW")
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'No JSON data received'}), 400
    
    data = pd.DataFrame([data])

    if data.empty:
        return jsonify({'error': 'No data provided'}), 400

    missing_required = [field for field in REQUIRED_FIELDS if pd.isna(data[field].iloc[0])]
    if missing_required:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_required)}'}), 400
    
    
    for column in data.columns:
        if column in ['no_of_dependents', 'education', 'self_employed']:
            fill_value = most_frequent_values.get(column, 0)
            data[column] = data[column].fillna(fill_value)
            data[column] = data[column].infer_objects(copy=False)
        elif column not in ['loan_term', 'cibil_score']:
            fill_value = mean_values.get(column, 0) 
            data[column] = data[column].fillna(fill_value)
            data[column] = data[column].infer_objects(copy=False)

    data["Total assets"]=data["residential_assets_value"]+data["commercial_assets_value"]+data["luxury_assets_value"]+data["bank_asset_value"]
    

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