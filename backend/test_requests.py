import requests

url = 'http://127.0.0.1:5000/predict'
# Updated features list with representative values for all 16 features
data = {'features': ['Male', 'USA', 'Engineer', 'No', 'Yes', 'No', 5, 3, 2, 'No', 'Yes', 'Sometimes', 'High', 'Low', 'No', 'Yes']}
response = requests.post(url, json=data)

print(response.json())
