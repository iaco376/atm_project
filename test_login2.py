import requests

# Testăm mai întâi dacă serverul răspunde
try:
    response = requests.get('http://127.0.0.1:5050/ping')
    print("Test conexiune:", response.status_code, response.json())
except Exception as e:
    print("Eroare conexiune /ping:", e)

# Testăm login-ul
url = 'http://127.0.0.1:5050/login'
data = {
    "username": "ionel",
    "password": "alex12942"
}

try:
    response = requests.post(url, json=data)
    print("Status code:", response.status_code)
    print("Răspuns JSON:", response.json())
except Exception as e:
    print("Eroare la cererea către server:", e)
