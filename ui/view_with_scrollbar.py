from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QGridLayout
from PySide6.QtCore import Qt

class ViewWithScrollbar(QWidget):
    def __init__(self, viewer, axis, parent=None):
        super().__init__(parent)

        self.viewer = viewer
        self.viewer.setStyleSheet("background-color: black;")
        self.axis = axis

        self.slider = QSlider(Qt.Vertical)
        self.slider.setSingleStep(1)
        self.slider.setFixedWidth(16)   # 👈 keeps it slim like PACS
        self.slider.setPageStep(10)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        layout.addWidget(self.viewer, 0, 0)   # viewer expands
        layout.addWidget(self.slider, 0, 1)   # scrollbar stays narrow

        self.slider.valueChanged.connect(self.viewer.set_slice)
        self.viewer.sliceChanged.connect(self.slider.setValue)
        self.slider.hide()
