from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QProgressBar,
    QListWidget, QSplitter, QTreeWidget, QTreeWidgetItem, QApplication, QLabel, QGroupBox, QStackedLayout
)
import os
from ui.scout_viewer import ScoutViewer
from dicom.scan_utils import analyze_scan
from dicom.volume_loader import load_volume
from ui.mpr_viewer import MPRViewer
from ui.mpr_viewer import MPRViewer
# from ui.loading_overlay import LoadingOverlay
from dicom.volume_loader import load_volume
from dicom.orientation import orient_volume
from dicom.exporter import export_as_multiple_dicoms
from dicom.exporter import export_as_single_dicom, fix_orientation_for_dicom
import re
from PySide6.QtCore import QThread
from utils.worker import Worker




class CaseViewerPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedHeight(35)
        self.back_btn.clicked.connect(self.on_back)
        self.scan_tree = QTreeWidget()
        self.scan_tree.setHeaderHidden(True)
        self.scan_tree.itemClicked.connect(self.open_item)
        self.preview_container = QWidget()
        self.preview_stack = QStackedLayout(self.preview_container)
        self.scout_viewer = ScoutViewer()
        self.mpr_viewer = MPRViewer()
        self.preview_stack.addWidget(self.scout_viewer)  # index 0
        self.preview_stack.addWidget(self.mpr_viewer)    # index 1

        self.export_multi_btn = QPushButton("Multi-DICOM")
        self.export_multi_btn.setFixedHeight(30)
        self.export_multi_btn.setEnabled(False)
        self.export_multi_btn.clicked.connect(self.on_export_multiple)

        self.export_single_btn = QPushButton("Export Sinlge-DICOM")
        self.export_single_btn.setFixedHeight(30)
        self.export_single_btn.setEnabled(False)
        self.export_single_btn.clicked.connect(self.on_export_single)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()

        self.volume = None
        self.dicom_datasets = None
        self.patient_name = None
        self.patient_name_label = QLabel("")
        self.patient_name_label.setFixedHeight(30)
        


        splitter = QSplitter()
        splitter.addWidget(self.scan_tree)
        splitter.addWidget(self.preview_container)
        splitter.setStretchFactor(1, 1)

        top_bar = QWidget()
        top_bar.setFixedHeight(60)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        # Left side
        left_widget = QWidget()
        # left_widget.setFixedHeight(100)
        left_layout = QHBoxLayout(left_widget)
        left_layout.addWidget(self.back_btn)
        left_layout.setContentsMargins(5, 10, 5, 10)
        left_layout.setSpacing(10)
        top_layout.addWidget(left_widget)
        # Right side
        export_group = QGroupBox("Export")
        export_layout = QHBoxLayout(export_group)
        export_layout.addWidget(self.export_multi_btn)
        export_layout.addWidget(self.export_single_btn)
        export_layout.setContentsMargins(5, 5, 5, 5)
        export_layout.setSpacing(5)
        top_layout.addWidget(export_group)
        top_layout.addWidget(self.patient_name_label)
        # Add stretch to push right to the right
        top_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top_bar)
        layout.addWidget(self.progress_bar)
        layout.addWidget(splitter)
    
    def on_back(self):
            self.scout_viewer.hide()
            self.mpr_viewer.hide()
            self.export_multi_btn.setEnabled(False)
            self.export_single_btn.setEnabled(False)
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

    def on_volume_loaded(self, result):
        volume, dicom_datasets = result

        volume = orient_volume(volume, dicom_datasets[0])

        self.current_volume = volume
        self.dicom_datasets = dicom_datasets
        # self.patient_name_label.setText(self.patient_name)
        self.export_multi_btn.setEnabled(True)
        self.export_single_btn.setEnabled(True)
        self.mpr_viewer.set_volume(volume)
        self.preview_stack.setCurrentIndex(1)

        self.progress_bar.hide()

        self.thread.quit()
        self.thread.wait()

    def open_item(self, item, _):
        scan_path = item.data(0, 1)
        self.preview_stack.setCurrentIndex(2)
        self.patient_name_label.setText(self.patient_name)

        if not scan_path:
            return

        info = analyze_scan(scan_path)

        def transform_name(raw_string):
            parts = raw_string.split('^')
            
            if len(parts) == 2:
                part1 = parts[0] # "383331Mahmoud Salah-Eldin"
                part2 = parts[1] # "El-Shimaa"
                part1_clean = re.sub(r'^\d+', '', part1)
                return f"{part2} {part1_clean}"
            return raw_string # Return original if format doesn't match

        if info["type"] == "scout":
            self.scout_viewer.show()
            self.scout_viewer.load_scan(scan_path)
            self.preview_stack.setCurrentIndex(0)
            self.patient_name_label.setText("Scout Image")            
            self.export_multi_btn.setEnabled(False)
            self.export_single_btn.setEnabled(False)            

        elif info["type"] == "cbct":

            patient = str(info["datasets"][0].get("PatientName", ""))
        
            patient_name = transform_name(patient)
            self.patient_name = patient_name
            self.patient_name_label.setText(self.patient_name)

            self.progress_bar.show()
            self.progress_bar.setValue(0)

            self.thread = QThread()
            self.worker = Worker(load_volume, info["datasets"], scan_path)

            self.worker.moveToThread(self.thread)

            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.finished.connect(self.on_volume_loaded)
            self.worker.error.connect(print)

            self.thread.started.connect(self.worker.run)

            self.thread.start()

    def on_export_multiple(self):
        if not self.dicom_datasets:
            print("No DICOM datasets loaded for export.")
            return

        output_dir = QFileDialog.getExistingDirectory(
             QApplication.activeWindow(),
            "Select Export Folder")

        if not output_dir:
            return

        self.progress_bar.show()
        self.progress_bar.setValue(0)

        self.thread = QThread()
        self.worker = Worker( export_as_multiple_dicoms, self.dicom_datasets, output_dir)

        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(lambda _: self.progress_bar.hide())
        self.worker.error.connect(print)

        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def on_export_single(self):
        if not self.dicom_datasets:
            print("No DICOM datasets loaded")
            return

        volume_for_export = fix_orientation_for_dicom(self.current_volume)
        vol_name = self.patient_name if self.patient_name else "cbct_volume"

        file_path, _ = QFileDialog.getSaveFileName(
            QApplication.activeWindow(),
            "Export as Single DICOM",
            f"{vol_name} DICOM.dcm",
            "DICOM Files (*.dcm)"
        )

        if not file_path:
            return

        export_as_single_dicom(self.dicom_datasets, volume_for_export, file_path)
