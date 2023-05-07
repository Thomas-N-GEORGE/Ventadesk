"""Status update dialog window."""

from PyQt6.QtWidgets import (
    QDialog,
)

from api_connect import api_update_order_status
from pui.status_update_dialog import Ui_Dialog
from pui.information import Ui_Dialog as Ui_Inf_Dialog
from pui.connexion import Ui_Dialog as Ui_connect


class StatusDialog(Ui_Dialog, QDialog):
    """Render compiled to Python status update dialog box."""

    def __init__(self, app, order):
        super().__init__()

        self.setupUi(self)
        self.setup_links()
        self.app = app
        self.order = order
        self.buttonBox.hide()

    def get_status_from_checkboxes(self):
        """Get new status from checkboxes"""

        new_status = None
        if self.radio_status_AA.isChecked():
            new_status = "AA"
        elif self.radio_status_AN.isChecked():
            new_status = "AN"
        elif self.radio_status_AP.isChecked():
            new_status = "AP"
        elif self.radio_status_CT.isChecked():
            new_status = "CT"
        elif self.radio_status_EX.isChecked():
            new_status = "EX"
        elif self.radio_status_CR.isChecked():
            new_status = "CR"
        elif self.radio_status_PE.isChecked():
            new_status = "PE"
        elif self.radio_status_TA.isChecked():
            new_status = "TA"

        return new_status

    def setup_links(self):
        """Links."""

        self.comment_text_edit.textChanged.connect(self.buttonBox.show)
        self.buttonBox.accepted.connect(self.update_order_status)
        self.buttonBox.rejected.connect(self.reject)

    def update_order_status(self):
        """Send info to api module."""

        is_updated = False

        if (
            self.comment_text_edit.toPlainText() == ""
            or self.get_status_from_checkboxes() is None
        ):
            info = InfoWindow(
                "Informations non validées. Veuillez noter un commentaire et choisir un statut."
            )
            info.exec()

        else:
            print(f'Order_id : {self.order["id"]}')
            print("new_status : ", self.get_status_from_checkboxes())
            print("new_comment : ", self.comment_text_edit.toPlainText())

            is_updated = api_update_order_status(
                app=self.app,
                order_id=self.order["id"],
                new_status=self.get_status_from_checkboxes(),
                comment=self.comment_text_edit.toPlainText(),
            )

            if is_updated:
                info_text = "Statut et commentaire envoyés avec succès."
            else:
                info_text = "Échec de la mise à jour de la commande."

            info = InfoWindow(info_text)
            info.exec()

        self.accept()

        # refresh main app
        if is_updated:
            self.app.refresh() 


class InfoWindow(Ui_Inf_Dialog, QDialog):
    """information dialog window."""

    def __init__(self, text):
        """Initialize."""

        super().__init__()
        self.setupUi(self)
        self.setModal(True)
        self.content.setText(text)
        self.setup_links()

    def setup_links(self):
        """Links."""

        self.btn_ok.clicked.connect(self.accept)


class ConnectDialog(Ui_connect, QDialog):
    """Connexion dialog box."""

    def __init__(self, app):
        """Initialize."""

        super().__init__()
        self.setupUi(self)
        self.setModal(True)
        self.app = app
        # self.show()
        self.setup_links()

    def setup_links(self):
        """Links."""

        self.btn_connect.clicked.connect(self.return_values)
        self.btn_abort.clicked.connect(self.reject)

    def return_values(self):
        """Slot to return entred values to app."""

        self.app.email = self.email_edit.text()
        self.app.password = self.password_edit.text()
        self.accept()
