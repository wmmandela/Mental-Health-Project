import requests

url = 'http://127.0.0.1:5000/predict'

def test_predict(features):
    data = {'features': features}
    response = requests.post(url, json=data)
    print(f"Input: {features}")
    print(f"Response: {response.status_code} - {response.json()}")
    print('-' * 40)

if __name__ == '__main__':
    # Valid input test with representative values for all 16 features
    test_predict(['Male', 'USA', 'Engineer', 'No', 'Yes', 'No', 5, 3, 2, 'No', 'Yes', 'Sometimes', 'High', 'Low', 'No', 'Yes'])

    # Invalid input tests
    test_predict(['invalid', 1.2, 3.0, 0.9])  # string in features
    test_predict([])  # empty features
    test_predict([0.5, 1.2])  # fewer features than expected
    test_predict(None)  # None as features
    test_predict([0.5, 1.2, 3.0, 0.9, 5.0])  # more features than expected
