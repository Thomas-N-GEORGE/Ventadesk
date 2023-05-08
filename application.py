"""Our main window application."""


import json
from datetime import datetime
from dateutil.parser import parse

from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QPushButton,
    QListWidgetItem,
)

from pui.if_ventadesk2 import Ui_MainWindow
from dialogs import StatusDialog, ConnectDialog, InfoDialog

from api_connect import (
    api_login,
    api_fetch_orders,
    api_fetch_customer,
    api_fetch_conversation,
    api_send_message,
)
from orders_payload import ORDERS_PAYLOAD, CONVERSATION_PAYLOAD
from utils import status_full_name


class AppWindow(Ui_MainWindow, QMainWindow):
    """Render compiled to Python IF."""

    def __init__(self):
        """Initialize."""

        super().__init__()
        self.email = None
        self.password = None
        self.user = None
        self.is_logged = False

        self.setupUi(self)
        self.setup_links()
        self.statusbar.showMessage(f"Non connecté(e)")
        self.tab_conversation.setEnabled(False)

        self.open_login_dialog()  # show login dialog at start

    def setup_links(self):
        """Connect signals and slots."""

        self.loginAct.triggered.connect(self.open_login_dialog)
        self.quitAct.triggered.connect(self.close)

    def open_login_dialog(self):
        """Enable login dialog."""

        # open connect dialog box
        connect_dialog = ConnectDialog(self)
        connect_dialog.accepted.connect(self.login)
        connect_dialog.exec()

    def login(self):
        """Slot to login to API."""

        self.is_logged, self.user = api_login(email=self.email, password=self.password)
        if self.is_logged:
            self.statusbar.showMessage(f"Connecté(e), bienvenue {self.user.first_name}")
            self.orders_load_and_display()
        else:
            self.open_login_dialog()

    def orders_load_and_display(self):
        """Load orders and populate to display."""

        orders = api_fetch_orders(self)

        for order in orders["results"]:
            # Order label
            label = QLabel()
            date = parse(order["date_created"])
            date_str = datetime.strftime(date, "%d-%m-%Y")

            # Order owner / customer.
            customer = api_fetch_customer(self, order["customer_account"])
            if customer and customer["count"] > 0:
                customer = customer["results"][0]
                print(
                    f'customer for {order["ref_number"]} : {customer["first_name"]} {customer["last_name"]}'
                )
                customer_info = (
                    f'Client(e) : {customer["first_name"]} {customer["last_name"]}'
                )
            else:
                customer = {}
                customer_info = ""

            label.setText(
                f'Commande n° {order["ref_number"]}\nstatut : {status_full_name(order["status"])}\ndatée du {date_str}\n'
                + customer_info
            )
            label.adjustSize()
            self.order_list_container.layout().addWidget(label)

            # Order owner / customer contact button.
            btn_contact = QPushButton()
            btn_contact.setText("contacter le client")
            # see if we can deliver this owner / owner_id in API payload ??
            # btn_contact.clicked.connect(lambda *_, o=order: self.open_order_conversation(o["owner"]))
            # btn_contact.clicked.connect(lambda *_, o=order: self.conversation_load_and_display(o))
            btn_contact.clicked.connect(
                lambda *_, c=customer: self.conversation_load_and_display(c)
            )
            self.order_list_container.layout().addWidget(btn_contact)

            # Order detail button.
            btn_detail = QPushButton()
            btn_detail.setText("détail de la commande")
            btn_detail.clicked.connect(
                lambda *_, o=order, c=customer: self.order_detail_display(o, c)
            )
            self.order_list_container.layout().addWidget(btn_detail)

    def order_detail_display(self, order: dict, customer: dict):
        """Display order details."""

        self.order_title.setText(f'Commande n° {order["ref_number"]}')
        self.order_details.clear()

        # Date.
        item = QListWidgetItem()
        date = parse(order["date_created"])
        date_str = datetime.strftime(date, "%d-%m-%Y")
        item.setText(f"Créée le {date_str}")
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.order_details.addItem(item)

        # Status.
        item = QListWidgetItem()
        item.setText(f'STATUT : {status_full_name(order["status"])}')
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.order_details.addItem(item)

        # Comment.
        try:
            comment = order["comment_set"][0]["content"]
        except:
            comment = ""

        item = QListWidgetItem()
        item.setText(f"COMMENTAIRE : {comment}")
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.order_details.addItem(item)

        # Customer.
        item = QListWidgetItem()
        if len(customer) > 0:
            item.setText(
                f'Client(e) : {customer["first_name"]} {customer["last_name"]}'
            )
        else:
            item.setText(f"Client(e) : ")
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.order_details.addItem(item)

        self.order_details.addItem("\n")

        # Order line items
        self.order_details.addItem("PRODUITS : ")
        for line_item in order["lineitem_set"]:
            item = QListWidgetItem()
            item.setText(
                f'{line_item["product"]}  Qté : {line_item["quantity"]}  Prix {line_item["price"]} HT'
            )
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            self.order_details.addItem(item)

        self.order_details.addItem("\n")

        # price details
        item = QListWidgetItem()
        item.setText(f'Prix total HT : {order["total_price"]}')
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.order_details.addItem(item)

        item = QListWidgetItem()
        item.setText(f'TVA: {order["vat_amount"]}')
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.order_details.addItem(item)

        item = QListWidgetItem()
        item.setText(f'Montant TTC: {order["incl_vat_price"]}')
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.order_details.addItem(item)

        # update button target
        self.btn_update_status.disconnect()
        self.btn_update_status.clicked.connect(
            lambda *_, o=order: self.order_status_dialog(o)
        )

    def order_status_dialog(self, order: dict):
        """Open update status dialog box."""

        status_dialog = StatusDialog(self, order)
        status_dialog.exec()

    def refresh(self):
        """Clear and reload order and order detail windows."""

        while not self.order_list_container.isEmpty():
            item = self.order_list_container.takeAt(0)
            item.widget().setParent(None)

        self.order_details.clear()

        self.login()

    def make_message_label(self, message: dict, customer: dict) -> QLabel:
        """Construct label to display message."""

        label = QLabel()
        date = parse(message["date_created"])
        date_str = datetime.strftime(date, "%d-%m-%Y")
        if message["author"] == self.user.email:
            author_wrote = "Vous avez écrit :"
        else:
            author_wrote = f'{customer["first_name"]} {customer["last_name"]} a écrit :'
        m_text = f'\n{author_wrote}\n{message["content"]}\nle {date_str}\n'
        label.setText(m_text)

        return label

    def conversation_load_and_display(self, customer: dict):
        """Open conversation with customer tab."""

        # clear display
        while not self.message_list_container.isEmpty():
            item = self.message_list_container.takeAt(0)
            item.widget().setParent(None)

        # Populate with messages and show conversation tab.
        # conversation = json.loads(CONVERSATION_PAYLOAD, strict=False)
        conversation = api_fetch_conversation(self, customer=customer)

        self.label_conversation_title.setText(conversation["subject"])

        for message in conversation["message_set"]:
            label = self.make_message_label(message, customer)
            if (
                # message["author"] == "jean.lancien@ventalis.com"
                message["author"]
                == self.user.email
            ):
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

            self.message_list_container.layout().addWidget(label)

        self.tab_conversation.setEnabled(True)
        self.tabWidget.setCurrentWidget(self.tab_conversation)

        # connect send message button
        self.btn_send_message.disconnect()
        self.btn_send_message.clicked.connect(
            lambda *_, co=conversation, cu=customer: self.send_message(co, cu)
        )

    def send_message(self, conversation: dict, customer: dict):
        """Send message to customer."""

        print(self.new_message_edit.toPlainText())
        message = self.new_message_edit.toPlainText()

        if message == "":
            info_dialog = InfoDialog("Votre message est vide.")
            info_dialog.exec()

        sent = api_send_message(self, conversation=conversation, content=message)

        if not sent:
            info_dialog = InfoDialog("Message non envoyé")
            info_dialog.exec()
        else:
            self.new_message_edit.clear()
            self.conversation_load_and_display(customer)
