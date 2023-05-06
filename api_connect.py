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

    data = {"username": email, "password": password}
    r = requests.post(API_TOKEN_URL, data=data)

    print("status : ", r.status_code)
    print("text : ", r.text)
    print("text type : ", type(r.text))

    if r.status_code == 200:
        response = json.loads(r.text, strict=False)

        # Check if user has employee role
        if response["role"] == "EMPLOYEE":
            user = User(
                token=response["token"],
                user_id=response["user_id"],
                email=response["email"],
                role=response["role"],
            )

            is_completed, user = user.api_complete_user()
            if is_completed:
                return True, user

    return False, None



class User:
    """User class."""

    def __init__(
        self,
        user_id,
        email,
        role,
        token=None,
        first_name=None,
        last_name=None,
        reg_number=None,
        conversation_set=None
    ):
        """Initilaize."""

        self.user_id = user_id
        self.email = email
        self.role = role
        self.token = token
        self.first_name = first_name
        self.last_name = last_name
        self.reg_number = reg_number
        self.conversation_set = conversation_set

    def api_complete_user(self):
        """Complete user info from api."""

        url = API_URL + "users/" + str(self.user_id)
        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(url, headers=headers)
        
        print("status : ", r.status_code)
        print("text : ", r.text)
        print("text type : ", type(r.text))

        if r.status_code == 200:
            response = json.loads(r.text, strict=False)
            self.first_name = response["first_name"]
            self.last_name = response["last_name"]
            self.reg_number = response["reg_number"]
            self.conversation_set = response["conversation_set"]

            return True, self
        
        return False, self
