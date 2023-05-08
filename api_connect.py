"""Our API connection module."""

import json
import requests
from config import API_URL, API_TOKEN_URL


def api_login(email, password):
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
                password=password,
                role=response["role"],
            )

            is_completed, user = user.api_complete_user()
            if is_completed:
                return True, user

    return False, None


class User:
    """User class built with API data."""

    def __init__(
        self,
        user_id,
        email,
        password,
        role,
        token=None,
        first_name=None,
        last_name=None,
        reg_number=None,
        conversation_set=None,
    ):
        """Initilaize."""

        self.user_id = user_id
        self.email = email
        self.password = password
        self.role = role
        self.token = token
        self.first_name = first_name
        self.last_name = last_name
        self.reg_number = reg_number
        self.conversation_set = conversation_set

    def api_complete_user(self):
        """Complete user info from api."""

        url = API_URL + "users/" + str(self.user_id)
        headers = {"Authorization": f"token {self.token}"}
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


def api_fetch_orders(app) -> dict:
    """GET orders related to employee, from API."""

    url = API_URL + "user_orders/"
    headers = {"Authorization": f"token {app.user.token}"}
    data = {"username": f"{app.user.email}", "password": f"{app.user.password}"}
    r = requests.get(url, headers=headers, data=data)

    print("status : ", r.status_code)
    print("text : ", r.text)
    print("text type : ", type(r.text))

    if r.status_code != 200:
        return

    return json.loads(r.text, strict=False)


def api_update_order_status(app, order_id, new_status, comment) -> bool:
    """POST new order comment and PUT new status to order."""

    url = API_URL + "comments/"
    headers = {"Authorization": f"token {app.user.token}"}
    # api fields : "content", "order_id"
    data = {
        "username": f"{app.user.email}",
        "password": f"{app.user.password}",
        "order_id": order_id,
        "content": comment,
    }
    r = requests.post(url, headers=headers, data=data)

    print("comment create status_code : ", r.status_code)
    print("comment create : ", r.text)
    print("text type : ", type(r.text))

    if r.status_code != 201:  # created
        return False

    url = API_URL + "orders/" + str(order_id) + "/"
    headers = {"Authorization": f"token {app.user.token}"}
    # api fields : "status"
    data = {
        "username": f"{app.user.email}",
        "password": f"{app.user.password}",
        "status": new_status,
    }
    r = requests.put(url, headers=headers, data=data)

    print("status update order : ", r.status_code)
    print("text update order : ", r.text)
    print("text type : ", type(r.text))

    return r.status_code == 200

def api_fetch_customer(app, customer_account):
    """GET customer detail from API, querying by related customer account id."""

    url = API_URL + "users/" + f'?customer_account={str(customer_account)}'
    headers = {"Authorization": f'token {app.user.token}'}
    data = {"username": f'{app.user.email}', "password": f'{app.user.password}'}
    r = requests.get(url, headers=headers, data=data)

    print("status : ", r.status_code)
    print("text : ", r.text)
    print("text type : ", type(r.text))

    if r.status_code != 200:
        return

    return json.loads(r.text, strict=False)

def api_fetch_conversation(app, customer):
    """GET customer related conversation from API."""

    # 
    # if (
    #     len(customer) == 0
    #     or "conversation_set" not in customer
    #     or len(customer["conversation_set"]) == 0
    # ):
    #     return

    url = API_URL + "conversations/" + str(customer["conversation_set"][0])
    headers = {"Authorization": f"token {app.user.token}"}
    data = {"username": f'{app.user.email}', "password": f'{app.user.password}'}
    r = requests.get(url, headers=headers, data=data)

    print("status : ", r.status_code)
    print("text : ", r.text)
    print("text type : ", type(r.text))

    if r.status_code != 200:
        return

    return json.loads(r.text, strict=False)

def api_send_message(app, conversation, content) -> bool:
    """POST API new message."""

    url = API_URL + "messages/"
    headers = {"Authorization": f"token {app.user.token}"}
    # api fields : "content", "conversation_id", "author"
    data = {
        "username": f"{app.user.email}",
        "password": f"{app.user.password}",
        "conversation_id": conversation["id"],
        "content": content,
    }
    r = requests.post(url, headers=headers, data=data)

    print("comment create status_code : ", r.status_code)
    print("comment create : ", r.text)
    print("text type : ", type(r.text))

    return r.status_code == 201  # created
