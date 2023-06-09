"""Our program entry point."""

from PyQt6.QtWidgets import (
    QApplication,
)

import os
import sys

basedir = os.path.dirname(__file__)

# from application import AppWindow
from .application import AppWindow


def main():
    """Main application."""

    app = QApplication(sys.argv)  # App object
    win = AppWindow()
    win.show()  # Show window
    app.exec()  # Run app


if __name__ == "__main__":
    main()
