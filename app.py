import sys
from PySide6.QtWidgets import QApplication
from database.db import init_db
from dicom.scanner import scan_root
from ui.main_window import MainWindow

ROOT_FOLDER = "G:\Projects\Py Projects\VolumeData"

init_db()
scan_root(ROOT_FOLDER)

app = QApplication(sys.argv)
win = MainWindow()
win.resize(900, 600)
win.show()
sys.exit(app.exec())
