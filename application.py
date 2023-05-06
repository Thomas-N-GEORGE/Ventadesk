"""Our main window application."""


import typing
import os
import sys
import json
from datetime import datetime
from dateutil.parser import parse

from PyQt6 import QtCore, uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QLabel,
    QPushButton,
    QLineEdit,
    QTreeWidgetItem,
    QWidget,
)


from pui.if_ventadesk2 import Ui_MainWindow
from status_dialog import StatusDialog

from api_connect import login
from orders_payload import ORDERS_PAYLOAD, CONVERSATION_PAYLOAD


class AppWindow(Ui_MainWindow, QMainWindow):
    """Render compiled to Python IF."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # TODO
        # self.setup_links()
        self.tab_conversation.setEnabled(False)
        self.load_orders(ORDERS_PAYLOAD)

    def load_orders(self, orders: dict):
        """Populate orders."""

        for order in orders["results"]:
            # order label
            label = QLabel()
            date = parse(order["date_created"])
            date_str = datetime.strftime(date, "%d-%m-%Y")
            label.setText(
                f'Commande n° {order["ref_number"]}\nstatut : {order["status"]}\ndatée du {date_str}'
            )
            label.adjustSize()
            self.order_list_container.layout().addWidget(label)

            # order owner contact button
            btn_contact = QPushButton()
            btn_contact.setText("contacter le client")
            # see if we can deliver this owner / owner_id in API payload ??
            # btn_contact.clicked.connect(lambda *_, o=order: self.open_order_conversation(o["owner"]))
            btn_contact.clicked.connect(lambda *_, o=order: self.order_conversation(o))
            self.order_list_container.layout().addWidget(btn_contact)

            # order dtail button
            btn_detail = QPushButton()
            btn_detail.setText("détail de la commande")
            btn_detail.clicked.connect(lambda *_, o=order: self.dispaly_order_detail(o))
            self.order_list_container.layout().addWidget(btn_detail)

    def dispaly_order_detail(self, order: dict):
        """Display order details."""

        self.order_title.setText(f'Commande n° {order["ref_number"]}')
        self.order_details.clear()

        # order detail:
        self.order_details.addItem(f'établie le {order["date_created"]}')
        self.order_details.addItem(f'statut {order["status"]}')
        try:
            self.order_details.addItem(
                f'Commentaire : {order["comment_set"][0]["content"]}'
            )
        except:
            self.order_details.addItem(f"Commentaire : ")

        # order line items
        for line_item in order["lineitem_set"]:
            self.order_details.addItem(
                f'{line_item["product"]} Qté : {line_item["quantity"]} Prix {line_item["price"]} HT'
            )

        # price details
        self.order_details.addItem(f'Prix total HT: {order["total_price"]}')
        self.order_details.addItem(f'TVA: {order["vat_amount"]}')
        self.order_details.addItem(f'Montant TTC: {order["incl_vat_price"]}')

        # update button target
        self.update_status.clicked.connect(
            lambda *_, o=order: self.order_status_dialog(o)
        )

    def order_status_dialog(self, order: dict):
        """Open update status dialog box."""

        status_dialog = StatusDialog(order)
        status_dialog.exec()

    def make_message_label(self, message: dict) -> QLabel:
        """Construct label to display message."""

        label = QLabel()
        date = parse(message["date_created"])
        date_str = datetime.strftime(date, "%d-%m-%Y")
        m_text = (
            f'\n{message["author"]} a écrit :\n{message["content"]}\n le {date_str}\n'
        )
        label.setText(m_text)

        return label

    def order_conversation(self, owner: dict):
        """Open conversation with customer tab."""

        # Populate with messages and show conversation tab.
        conversation = json.loads(CONVERSATION_PAYLOAD, strict=False)
        self.label_conversation_title.setText(conversation["subject"])
        
        for message in conversation["message_set"]:
            label = self.make_message_label(message)
            if message["author"] == "jean.lancien@ventalis.com":    # Get connected employee !
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

            self.message_list_container.layout().addWidget(label)

        self.tab_conversation.setEnabled(True)
        self.tabWidget.setCurrentWidget(self.tab_conversation)

        # connect send message button
        self.btn_send_message.clicked.connect(self.send_message)

    def send_message(self):
        """Call api send message"""

        # TODO
        # API POST
        print(self.new_message_edit.toPlainText())
        self.tab_conversation.setEnabled(False)
        self.tabWidget.setCurrentWidget(self.tab_orders)
