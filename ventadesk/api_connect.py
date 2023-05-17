"""Our API connection module."""

import json
import requests


from .config import API_URL, API_TOKEN_URL
from .dialogs.info_dialog import InfoDialog
from .dialogs.info_dialog import InfoDialog


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
        try:
            r = requests.get(url, headers=headers)
        except:
            api_connexion_error_dialog()
            return False, self
        try:
            r = requests.get(url, headers=headers)
        except:
            api_connexion_error_dialog()
            return False, self

        if r.status_code == 200:
            response = json.loads(r.text, strict=False)
            self.first_name = response["first_name"]
            self.last_name = response["last_name"]
            self.reg_number = response["reg_number"]
            self.conversation_set = response["conversation_set"]

            return True, self

        return False, self


def api_connexion_error_dialog(message="Erreur de connexion distante."):
    """Message box."""

    info_dialog = InfoDialog(message)
    info_dialog.exec()


def api_login(email, password):
    """Login function to connect to VentAPI."""

    data = {"username": email, "password": password}
    try:
        r = requests.post(API_TOKEN_URL, data=data)
    except:
        api_connexion_error_dialog()
        return False, None

    if r.status_code != 200:
        return False, None

    response = json.loads(r.text, strict=False)

    # Check if user has employee role
    if response["role"] != "EMPLOYEE":
        return False, None

    user = User(
        token=response["token"],
        user_id=response["user_id"],
        email=response["email"],
        password=password,
        role=response["role"],
    )

    # Fetch remaining user info from API.
    is_completed, user = user.api_complete_user()
    if is_completed:
        return True, user

    return False, None


def api_connexion_error_dialog(message="Erreur de connexion distante."):
    """Message box."""

    info_dialog = InfoDialog(message)
    info_dialog.exec()


def api_login(email, password):
    """Login function to connect to VentAPI."""

    data = {"username": email, "password": password}
    try:
        r = requests.post(API_TOKEN_URL, data=data)
    except:
        api_connexion_error_dialog()
        return False, None

    if r.status_code != 200:
        return False, None

    response = json.loads(r.text, strict=False)

    # Check if user has employee role
    if response["role"] != "EMPLOYEE":
        return False, None

    user = User(
        token=response["token"],
        user_id=response["user_id"],
        email=response["email"],
        password=password,
        role=response["role"],
    )

    # Fetch remaining user info from API.
    is_completed, user = user.api_complete_user()
    if is_completed:
        return True, user

    return False, None


def api_fetch_orders(app) -> dict:
    """GET orders related to employee, from API."""

    url = API_URL + "user_orders/"
    headers = {"Authorization": f"token {app.user.token}"}
    try:
        r = requests.get(url, headers=headers)
    except:
        api_connexion_error_dialog()
        return

    if r.status_code != 200:
        return

    return json.loads(r.text, strict=False)


def api_update_order_status(app, order_id, new_status, comment) -> bool:
    """POST new order comment and PUT new status to order."""

    url = API_URL + "comments/"
    headers = {"Authorization": f"token {app.user.token}"}
    # api fields : "content", "order_id"
    data = {
        "order_id": order_id,
        "content": comment,
    }
    try:
        r = requests.post(url, headers=headers, data=data)
    except:
        api_connexion_error_dialog()
        return False
    try:
        r = requests.post(url, headers=headers, data=data)
    except:
        api_connexion_error_dialog()
        return False

    if r.status_code != 201:  # created
        return False

    url = API_URL + "orders/" + str(order_id) + "/"
    headers = {"Authorization": f"token {app.user.token}"}
    # api fields : "status"
    data = {
        "status": new_status,
    }
    r = requests.put(url, headers=headers, data=data)

    return r.status_code == 200


def api_fetch_customer(app, customer_account):
    """GET customer detail from API, querying by related customer account id."""

    url = API_URL + "users/" + f"?customer_account={str(customer_account)}"
    headers = {"Authorization": f"token {app.user.token}"}
    try:
        r = requests.get(url, headers=headers)
    except:
        api_connexion_error_dialog()
        return

    if r.status_code != 200:
        return

    return json.loads(r.text, strict=False)



def api_fetch_conversation(app, customer):
    """GET customer related conversation from API."""

    url = API_URL + "conversations/" + str(customer["conversation_set"][0])
    headers = {"Authorization": f"token {app.user.token}"}
    try:
        r = requests.get(url, headers=headers)
    except:
        api_connexion_error_dialog()
        return

    if r.status_code != 200:
        return

    return json.loads(r.text, strict=False)



def api_send_message(app, conversation, content) -> bool:
    """POST API new message."""

    url = API_URL + "messages/"
    headers = {"Authorization": f"token {app.user.token}"}
    # api fields : "content", "conversation_id", author is implicit to connexion.
    data = {
        "conversation_id": conversation["id"],
        "content": content,
    }
    try:
        r = requests.post(url, headers=headers, data=data)
    except:
        api_connexion_error_dialog()
        return
    try:
        r = requests.post(url, headers=headers, data=data)
    except:
        api_connexion_error_dialog()
        return

    return r.status_code == 201  # created
