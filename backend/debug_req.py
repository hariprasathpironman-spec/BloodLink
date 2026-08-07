import json
import urllib.request
import urllib.error

req = urllib.request.Request(
    'http://127.0.0.1:5000/api/auth/register/donor', 
    data=json.dumps({
        'name': 'Test2', 
        'email': 'test999@test.com', 
        'password': 'testpassword', 
        'blood_group': 'B+', 
        'state': 'TN', 
        'district': 'Madurai', 
        'age': 19, 
        'weight': 100, 
        'gender': 'Male'
    }).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}
)

try:
    res = urllib.request.urlopen(req)
    print(res.read().decode())
except urllib.error.HTTPError as e:
    print(e.read().decode())
except Exception as e:
    print(str(e))
