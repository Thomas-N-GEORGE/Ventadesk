"""Our API connection module."""

import json
import requests

# >>> import requests
# >>> r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
# >>> r.status_code
# 200
# >>> r.headers['content-type']
# 'application/json; charset=utf8'
# >>> r.encoding
# 'utf-8'
# >>> r.text
# '{"authenticated": true, ...'
# >>> r.json()
# {'authenticated': True, ...}

API_URL = "http://127.0.0.1:8000/api/"
API_TOKEN_URL = "http://127.0.0.1:8000/api/api-token-auth/"


def login(email, password):
    """Login function to connect to VentAPI."""

    data = {
        "username": email,
        "password": password
    }

    r = requests.post(API_TOKEN_URL, data=data)

    print("status : ", r.status_code)
    print("text : ", r.text)
    print("text type : ", type(r.text))

    if r.status_code == 200:
        return True
    
    return False
