"""Our main window application."""


import typing
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

import os
import sys
import json

from pui.if_ventadesk2 import Ui_MainWindow
from status_dialog import StatusDialog

from api_connect import login
from orders_payload import ORDERS_PAYLOAD


class AppWindow(Ui_MainWindow, QMainWindow):
    """Render compiled to Python IF."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # TODO
        # self.setup_links()
        
        self.load_orders(ORDERS_PAYLOAD)

    def load_orders(self, orders: dict):
        """Populate orders."""

        for order in ORDERS_PAYLOAD["results"]:
            # order label
            label = QLabel()
            label.setText(
                f'Commande n° {order["ref_number"]}, statut {order["status"]} établie le {order["date_created"]}'
            )
            label.adjustSize()
            self.order_list_container.layout().addWidget(label)

            # order owner contact button
            btn_contact = QPushButton()
            btn_contact.setText("contacter le client")
            # see if we can deliver this owner / owner_id in API payload ??
            # btn_contact.clicked.connect(lambda *_, o=order: self.open_order_conversation(o["owner"])) 
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
            self.order_details.addItem(f'Commentaire : {order["comment_set"][0]["content"]}')
        except:
            self.order_details.addItem(f'Commentaire : ')


        # order line items
        for line_item in order["lineitem_set"]:
            self.order_details.addItem(f'{line_item["product"]} Qté : {line_item["quantity"]} Prix {line_item["price"]} HT')

        # price details
        self.order_details.addItem(f'Prix total HT: {order["total_price"]}')
        self.order_details.addItem(f'TVA: {order["vat_amount"]}')
        self.order_details.addItem(f'Montant TTC: {order["incl_vat_price"]}')

        # update button target
        self.update_status.clicked.connect(lambda *_, o=order: self.open_status_dialog(o))

    def open_status_dialog(self, order:dict):
        """open update status dialog box."""

        status_dialog = StatusDialog(order)
        status_dialog.exec()
