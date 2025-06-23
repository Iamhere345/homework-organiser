import sys
from PySide6.QtWidgets import QApplication

from app import HomeworkOrganiser


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = HomeworkOrganiser()

    sys.exit(app.exec())
