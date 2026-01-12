from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QListWidget, QSplitter, QTreeWidget, QTreeWidgetItem
)
import os
from ui.scout_viewer import ScoutViewer
from dicom.scan_utils import analyze_scan
from dicom.volume_loader import load_volume
from ui.mpr_viewer import MPRViewer
from PySide6.QtWidgets import QWidget, QStackedLayout
from ui.scout_viewer import ScoutViewer
from ui.mpr_viewer import MPRViewer
from ui.loading_overlay import LoadingOverlay
from dicom.volume_loader import load_volume
from dicom.orientation import orient_volume
from dicom.exporter import export_as_multiple_dicoms
from PyQt5.QtWidgets import QFileDialog
# lol

class CaseViewerPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.back_btn = QPushButton("← Back to Cases")
        self.back_btn.clicked.connect(self.on_back)
        self.scan_tree = QTreeWidget()
        self.scan_tree.setHeaderHidden(True)
        self.scan_tree.itemClicked.connect(self.open_item)
        self.preview_container = QWidget()
        self.preview_stack = QStackedLayout(self.preview_container)
        self.scout_viewer = ScoutViewer()
        self.mpr_viewer = MPRViewer()
        self.loading_overlay = LoadingOverlay()
        self.preview_stack.addWidget(self.scout_viewer)  # index 0
        self.preview_stack.addWidget(self.mpr_viewer)    # index 1
        self.preview_stack.addWidget(self.loading_overlay)

        splitter = QSplitter()
        splitter.addWidget(self.scan_tree)
        splitter.addWidget(self.preview_container)
        splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.back_btn)
        layout.addWidget(splitter)
    
    def on_back(self):
            self.scout_viewer.hide()
            self.mpr_viewer.hide()
            self.main.go_back()

    def load_case(self, case_path):
        self.case_path = case_path
        self.scan_tree.clear()

        for date_folder in sorted(os.listdir(case_path)):
            date_path = os.path.join(case_path, date_folder)
            if not os.path.isdir(date_path):
                continue

            date_item = QTreeWidgetItem([date_folder])
            self.scan_tree.addTopLevelItem(date_item)

            for scan in sorted(os.listdir(date_path)):
                scan_path = os.path.join(date_path, scan)
                if not os.path.isdir(scan_path):
                    continue

                scan_item = QTreeWidgetItem([scan])
                scan_item.setData(0, 1, scan_path)  # store full path
                date_item.addChild(scan_item)

            date_item.setExpanded(True)

    def open_item(self, item, _):
        scan_path = item.data(0, 1)
        self.preview_stack.setCurrentIndex(2)

        if not scan_path:
            return

        info = analyze_scan(scan_path)

        if info["type"] == "scout":
            self.scout_viewer.show()
            self.scout_viewer.load_scan(scan_path)
            self.preview_stack.setCurrentIndex(0)

        elif info["type"] == "cbct":

            self.loading_overlay.show()
            self.preview_stack.setCurrentIndex(2)

            volume, dicom_datasets  = load_volume(info["datasets"], scan_path)
            volume = orient_volume(volume, dicom_datasets[0])
            
            self.mpr_viewer.show()
            self.mpr_viewer.set_volume(volume)
            self.preview_stack.setCurrentIndex(1)
            self.loading_overlay.hide()

        output_dir = r"G:\Projects\Py Projects\export_test"
        export_as_multiple_dicoms( dicom_datasets, output_dir)
        