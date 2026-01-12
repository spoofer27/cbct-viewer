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
# from dicom.exporter import (
#     export_as_single_dicom,
#     export_as_multiple_dicoms
# )
from dicom.exporter import export_as_multiple_dicoms
from PyQt5.QtWidgets import QFileDialog


class CaseViewerPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        self.back_btn = QPushButton("← Back to Cases")
        # self.back_btn.clicked.connect(self.main.go_back)
        self.back_btn.clicked.connect(self.on_back)

        # self.scan_list = QListWidget()
        # self.scan_list.itemClicked.connect(self.open_scan)

        self.scan_tree = QTreeWidget()
        self.scan_tree.setHeaderHidden(True)
        self.scan_tree.itemClicked.connect(self.open_item)


        # self.preview = ScoutViewer()
        self.preview_container = QWidget()
        self.preview_stack = QStackedLayout(self.preview_container)

        self.scout_viewer = ScoutViewer()
        self.mpr_viewer = MPRViewer()
        self.loading_overlay = LoadingOverlay()
        # self.loading_overlay.raise_()

        self.preview_stack.addWidget(self.scout_viewer)  # index 0
        self.preview_stack.addWidget(self.mpr_viewer)    # index 1
        self.preview_stack.addWidget(self.loading_overlay)

        splitter = QSplitter()
        # splitter.addWidget(self.scan_list)
        # splitter.addWidget(self.preview)
        splitter.addWidget(self.scan_tree)
        # splitter.addWidget(self.preview)
        splitter.addWidget(self.preview_container)

        splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self)
        layout.addWidget(self.back_btn)
        layout.addWidget(splitter)
    
    def on_back(self):
        # remove and delete every widget in the preview stack
        # while self.preview_stack.count():
        #     w = self.preview_stack.widget(0)
        #     self.preview_stack.removeWidget(w)
        #     w.deleteLater()
            # drop references to viewers so they can be recreated later if needed
            self.scout_viewer.hide()
            self.mpr_viewer.hide()
            self.main.go_back()


    def load_case(self, case_path):
        # self.case_path = case_path
        # self.scan_list.clear()

        # for folder in os.listdir(case_path):
        #     self.scan_list.addItem(folder)
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


    # def open_scan(self, item):
    # def open_item(self, item, _):   
        # scan_path = os.path.join(self.case_path, item.text())
        # self.preview.load_scan(scan_path)
        # scan_path = item.data(0, 1)
        # if not scan_path:
        #     return  # clicked a date, not a scan

        # # self.preview.load_scan(scan_path)
        # info = analyze_scan(scan_path)

        # if info["type"] == "scout":
        #     self.preview.load_scan(scan_path)

        # elif info["type"] == "cbct":
        #     volume = load_volume(info["files"])

        #     self.mpr = MPRViewer()
        #     self.mpr.set_volume(volume)

        #     self.preview.layout().replaceWidget(
        #         self.preview, self.mpr
        #     )
        #     self.preview.deleteLater()
        #     self.preview = self.mpr
    
    
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
            # volume = load_volume(info["files"])
            # self.mpr_viewer.set_volume(volume)
            # self.preview_stack.setCurrentIndex(1)

            self.loading_overlay.show()
            self.preview_stack.setCurrentIndex(2)

            # volume, ref_ds = load_volume(info["datasets"], scan_path)
            volume, dicom_datasets  = load_volume(info["datasets"], scan_path)
            volume = orient_volume(volume, dicom_datasets[0])

            
            print(info["type"], len(info["datasets"]))
            self.mpr_viewer.show()
            self.mpr_viewer.set_volume(volume)
            self.preview_stack.setCurrentIndex(1)
            self.loading_overlay.hide()

        output_dir = r"G:\Projects\Py Projects\export_test"
        export_as_multiple_dicoms( dicom_datasets, output_dir)
        
    # def on_export_multi(self):
    #     output_dir = QFileDialog.getExistingDirectory(
    #         self, "Select Export Folder"
    #     )
    #     if not output_dir:
    #         return

    #     export_as_multiple_dicoms(
    #         self.volume,
    #         self.reference_datasets,
    #         output_dir
    #     )
    
    # def on_export_single(self):
    #     path, _ = QFileDialog.getSaveFileName(
    #         self, "Export DICOM",
    #         filter="DICOM Files (*.dcm)"
    #     )
    #     if not path:
    #         return

    #     export_as_single_dicom(
    #         self.volume,
    #         self.reference_datasets[0],
    #         path
    #     )
