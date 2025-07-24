import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPalette

from app import HomeworkOrganiser

if __name__ == "__main__":
    app = QApplication(sys.argv)

    pal = QPalette()

    mid_colour = pal.color(QPalette.ColorRole.Mid)
    pal.setColor(QPalette.ColorRole.Window, mid_colour)

    app.setPalette(pal)

    #app.setStyle("Fusion")

    window = QMainWindow()
    window.setWindowTitle("Homework Organiser")

    homework_organiser = HomeworkOrganiser()
    window.setCentralWidget(homework_organiser)
    
    window.resize(768, 480)
    window.show()

    sys.exit(app.exec())
