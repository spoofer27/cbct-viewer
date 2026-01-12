from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
import numpy as np
from PySide6.QtCore import Signal

class SliceViewer(QGraphicsView):
    sliceChanged = Signal(int)
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.volume = None
        self.axis = 0
        self.index = 0
        self.max_index = 0

        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def set_volume(self, volume, axis):
        self.volume = volume
        self.axis = axis
        self.index = volume.shape[axis] // 2
        self.max_index = volume.shape[axis] - 1
        self.update_slice()

    def wheelEvent(self, event):
        if self.volume is None:
            return

        delta = event.angleDelta().y() // 120
        self.index = max(
            0,
            min(self.volume.shape[self.axis] - 1, self.index + delta)
        )
        self.update_slice()
        self.sliceChanged.emit(self.index)

    def set_slice(self, index):
        if self.volume is None:
            return

        self.index = max(0, min(index, self.max_index))
        self.update_slice()


    def update_slice(self):
        if self.volume is None:
            return
    
        if self.axis == 0: # AXIAL
            img = self.volume[self.index, :, :]
             # flip Y so anterior is up
            # img = img[::-1, :]

        elif self.axis == 1: # CORONAL
            img = self.volume[:, self.index, :]
            # flip Z (vertical) and X (horizontal)
            img = img[::-1, :]

        else: # SAGITTAL
            img = self.volume[:, :, self.index]
            # flip Z (vertical)
            img = img[::-1, ::-1]

        img = img.astype(np.float32)
        # img = (img - img.min()) / (img.ptp() + 1e-6) * 255
        img = (img - img.min()) / (np.ptp(img) + 1e-6) * 255
        img = img.astype(np.uint8)

        h, w = img.shape
        qimg = QImage(img.data, w, h, w, QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(qimg)

        self.scene.clear()
        self.scene.addPixmap(pix)
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
