from PySide6.QtWidgets import QFrame

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