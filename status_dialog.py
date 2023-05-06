"""Status update dialog window."""

from PyQt6.QtWidgets import (
    QDialog,
)

from pui.status_update_dialog import Ui_Dialog
from pui.information import Ui_Dialog as Ui_Inf_Dialog


class StatusDialog(Ui_Dialog, QDialog):
    """Render compiled to Python status update dialog box."""

    def __init__(self, order):
        super().__init__()

        self.setupUi(self)
        self.setup_links()
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
        elif self.radio_status_NT.isChecked():
            new_status = "NT"
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

        if self.comment_text_edit.toPlainText() == "" or self.get_status_from_checkboxes() is None:
            info = InfoWindow("Informations non validées. Veuillez noter un commentaire et choisir un statut.")
            info.exec()
            pass

        else:
            print(f'Order_id : {self.order["id"]}')
            print("new_status : ", self.get_status_from_checkboxes())
            print("new_comment : ", self.comment_text_edit.toPlainText())

        self.accept()


class InfoWindow(Ui_Inf_Dialog, QDialog):
    """information dialog window."""

    def __init__(self, text):
        super().__init__()
        self.setupUi(self   )
        self.content.setText(text)
        self.setup_links()
        self.btn_cancel.setDisabled(True)

    def setup_links(self):
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
