from PySide6.QtWidgets import (
    QMainWindow, QListWidget, QSplitter
)
import os
from ui.scout_viewer import ScoutViewer

class CaseWindow(QMainWindow):
    def __init__(self, case_path):
        super().__init__()
        self.setWindowTitle("Case Viewer")
        self.case_path = case_path

        self.list = QListWidget()
        self.list.itemClicked.connect(self.open_scan)

        self.preview = ScoutViewer()

        splitter = QSplitter()
        splitter.addWidget(self.list)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)
        self.load_scans()

    def load_scans(self):
        for folder in os.listdir(self.case_path):
            self.list.addItem(folder)

    def open_scan(self, item):
        scan_path = os.path.join(self.case_path, item.text())
        self.preview.load_scan(scan_path)
