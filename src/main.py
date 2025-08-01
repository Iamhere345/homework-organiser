import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PySide6.QtGui import QPalette

from app import HomeworkOrganiser
from menu import AppMenuBar

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # set palette to colours that better match OSX dark mode
    # TODO fix colours for light mode
    # TODO how does it look on windows?
    pal = QPalette()

    mid_colour = pal.color(QPalette.ColorRole.Mid)
    pal.setColor(QPalette.ColorRole.Window, mid_colour)
    app.setPalette(pal)

    # ! maintainability: if a consistent cross-platform style is needed uncomment this line
    #app.setStyle("Fusion")

    # initialise window
    window = QMainWindow()
    window.setWindowTitle("Homework Organiser")

    # add menu bar to app
    menu_bar = AppMenuBar()
    window.setMenuBar(menu_bar)

    # initialise application and set the app as the windows central widget
    homework_organiser = HomeworkOrganiser(menu_bar.tasks)
    window.setCentralWidget(homework_organiser)

    window.resize(768, 480)
    window.show()

    # run application, exit when the app returns
    sys.exit(app.exec())
