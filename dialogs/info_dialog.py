"""Utility info dialog class module."""


from PyQt6.QtWidgets import (
    QDialog,
)
from pui.information import Ui_Dialog

class InfoDialog(Ui_Dialog, QDialog):
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