from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import pydicom
import numpy as np
import cv2
import os

class ScoutViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Select a scan")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self._pixmap = None 

    def load_scan(self, scan_path):
        dicoms = [f for f in os.listdir(scan_path) if f.lower().endswith(".dcm")]
        if len(dicoms) != 1:
            self.label.setText("Not a scout image")
            self._pixmap = None
            return

        ds = pydicom.dcmread(os.path.join(scan_path, dicoms[0]))
        img = ds.pixel_array.astype(np.float32)

        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        img = img.astype(np.uint8)

        h, w = img.shape
        qimg = QImage(img.data, w, h, w, QImage.Format_Grayscale8)
        self._pixmap = QPixmap.fromImage(qimg)
        self._update_pixmap()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_pixmap()

    def _update_pixmap(self):
        if not self._pixmap:
            return

        scaled = self._pixmap.scaled(
            self.label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled)
        self.label.setStyleSheet("background-color: black;")

