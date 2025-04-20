from flask import Flask, request, jsonify
import joblib
import numpy as np

model = joblib.load('../models/best_model.joblib')
scaler = joblib.load('../models/scaler.pkl')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    features = np.array(data['features']).reshape(1, -1)

    scalable_features = features[:, [3, 4, 7, 8, 9, 10, 11]]
    non_scalable_features = np.delete(features, [3, 4, 7, 8, 9, 10, 11], axis=1)  # Остальные признаки

    scaled_features = scaler.transform(scalable_features)

    final_features = np.hstack((scaled_features, non_scalable_features))

    prediction = model.predict(final_features)
    result = int(prediction[0])

    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)