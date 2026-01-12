from PySide6.QtWidgets import QWidget, QGridLayout
from ui.slice_viewer import SliceViewer
from ui.view_with_scrollbar import ViewWithScrollbar

class MPRViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.axial_viewer = SliceViewer()
        self.axial_widget = ViewWithScrollbar(self.axial_viewer, axis=0)

        self.coronal_viewer = SliceViewer()
        self.coronal_widget = ViewWithScrollbar(self.coronal_viewer, axis=1)

        self.sagittal_viewer = SliceViewer()
        self.sagittal_widget = ViewWithScrollbar(self.sagittal_viewer, axis=2)

        layout = QGridLayout(self)

        layout.addWidget(self.axial_widget, 0, 0)
        layout.addWidget(self.coronal_widget, 0, 1)
        layout.addWidget(self.sagittal_widget, 1, 0)

    def set_volume(self, volume):
        self.volume = volume
        z, y, x = volume.shape

        self.axial_viewer.set_volume(volume, axis=0)
        self.axial_widget.slider.show()
        self.axial_widget.slider.setRange(0, z - 1)

        self.coronal_viewer.set_volume(volume, axis=1)
        self.coronal_widget.slider.show()
        self.coronal_widget.slider.setRange(0, y - 1)

        self.sagittal_viewer.set_volume(volume, axis=2)
        self.sagittal_widget.slider.show()
        self.sagittal_widget.slider.setRange(0, x - 1)
