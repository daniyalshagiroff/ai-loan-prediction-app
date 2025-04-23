import requests

url = 'http://127.0.0.1:5000/predict'
data = {
    "features": [0, 0, 1, 4100000, 12200000, 8, 417, 2700000, 2200000, 8800000, 3300000, 17000000]
}
res = requests.post(url, json=data)

print(res.json())