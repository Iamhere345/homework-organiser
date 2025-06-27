import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from app import HomeworkOrganiser

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Homework Organiser")

    homework_organiser = HomeworkOrganiser()
    window.setCentralWidget(homework_organiser)
    
    window.show()

    sys.exit(app.exec())
