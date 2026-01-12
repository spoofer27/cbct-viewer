from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class LoadingOverlay(QWidget):
    def __init__(self, parent=None, text="Loading scan..."):
        super().__init__(parent)
        print("Initializing LoadingOverlay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 160);
        """)

        label = QLabel(text)
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()

        self.hide()

    def resizeEvent(self, event):
        self.setGeometry(self.parent().rect())
