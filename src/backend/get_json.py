import requests


url = 'http://127.0.0.1:5000/predict'


data = {
    "no_of_dependents": 0,
    "education": 0,
    "self_employed": 1,
    "income_annum": None,
    "loan_amount": None,
    "loan_term": 4,
    "cibil_score": 500,
    "residential_assets_value": None,
    "commercial_assets_value": 2200000,
    "luxury_assets_value": 8800000,
    "bank_asset_value": None
}

# Преобразование в JSON и отправка POST-запроса
res = requests.post(url, json=data)

# Вывод результата
print(res.json())