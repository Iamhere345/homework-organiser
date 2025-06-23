import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

class HomeworkOrganiser(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Homework Organiser")

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
