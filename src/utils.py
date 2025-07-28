from PySide6.QtWidgets import QFrame, QMessageBox

class SeperatorLine(QFrame):
    def __init__(self, is_vertical: bool):
        super().__init__()
        super().setFrameShadow(QFrame.Shadow.Plain)
        super().setStyleSheet("background-color: palette(light); border: none;")

        if is_vertical:
            super().setFrameShape(QFrame.Shape.VLine)
            super().setFixedWidth(1)
        else:
            super().setFrameShape(QFrame.Shape.HLine)
            super().setFixedHeight(1)

class ErrorMessage(QMessageBox):
    def __init__(self, title: str, desc: str):
        super().__init__()

        super().setWindowTitle(title)
        super().setText(desc)
        super().setIcon(QMessageBox.Icon.Warning)

        super().setStandardButtons(QMessageBox.StandardButton.Ok)

        super().exec()