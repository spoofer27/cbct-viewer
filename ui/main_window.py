from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget
)
from ui.case_list_page import CaseListPage
from ui.case_viewer_page import CaseViewerPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("CBCT Case Browser")
        self.setWindowTitle("CBCT Viewer")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.case_list_page = CaseListPage(self)
        self.case_viewer_page = CaseViewerPage(self)

        self.stack.addWidget(self.case_list_page)   # index 0
        self.stack.addWidget(self.case_viewer_page) # index 1

        self.stack.setCurrentIndex(0)
    
    def open_case(self, case_path):
        self.case_viewer_page.load_case(case_path)
        self.stack.setCurrentIndex(1)

    def go_back(self):
        self.stack.setCurrentIndex(0)
    