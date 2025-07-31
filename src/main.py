import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PySide6.QtGui import QPalette

from app import HomeworkOrganiser
from menu import AppMenuBar

if __name__ == "__main__":
    app = QApplication(sys.argv)

    pal = QPalette()

    mid_colour = pal.color(QPalette.ColorRole.Mid)
    pal.setColor(QPalette.ColorRole.Window, mid_colour)

    app.setPalette(pal)

    #app.setStyle("Fusion")

    window = QMainWindow()
    window.setWindowTitle("Homework Organiser")

    menu_bar = AppMenuBar()
    window.setMenuBar(menu_bar)

    homework_organiser = HomeworkOrganiser(menu_bar.tasks)
    window.setCentralWidget(homework_organiser)

    window.resize(768, 480)
    window.show()

    sys.exit(app.exec())
