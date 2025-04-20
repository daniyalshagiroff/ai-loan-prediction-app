import requests

url = 'http://127.0.0.1:5000/predict'
data = {
    "features": [5, 0, 1, 9800000, 24200000, 20, 1000, 12400000, 8200000, 29400000, 5000000, 55000000]
}
res = requests.post(url, json=data)

print(res.json())