# from PySide6.QtWidgets import (
#     QMainWindow, QTableWidget, QTableWidgetItem,
#     QVBoxLayout, QWidget, QLineEdit
# )
from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget
)
from ui.case_list_page import CaseListPage
from ui.case_viewer_page import CaseViewerPage
# import sqlite3
# from database.db import DB_PATH
# from ui.case_window import CaseWindow

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

        # ------------- Previous code for reference -------------
    #     self.search = QLineEdit()
    #     self.search.setPlaceholderText("Search case...")
    #     self.search.textChanged.connect(self.load_cases)

    #     self.table = QTableWidget(0, 5)
    #     self.table.setHorizontalHeaderLabels(
    #         ["ID", "Name", "Age", "Gender", "Date"]
    #     )
    #     self.table.cellDoubleClicked.connect(self.open_case)

    #     layout = QVBoxLayout()
    #     layout.addWidget(self.search)
    #     layout.addWidget(self.table)

    #     container = QWidget()
    #     container.setLayout(layout)
    #     self.setCentralWidget(container)

    #     self.load_cases()

    # def load_cases(self):
    #     text = self.search.text()
    #     conn = sqlite3.connect(DB_PATH)
    #     c = conn.cursor()

    #     query = """
    #     SELECT id, name, age, gender, date, path FROM cases
    #     WHERE id LIKE ? OR name LIKE ?
    #     """
    #     rows = c.execute(query, (f"%{text}%", f"%{text}%")).fetchall()
    #     conn.close()

    #     self.table.setRowCount(0)
    #     for row in rows:
    #         row_idx = self.table.rowCount()
    #         self.table.insertRow(row_idx)
    #         for col, val in enumerate(row[:5]):
    #             self.table.setItem(row_idx, col, QTableWidgetItem(val))
    #         self.table.setRowHeight(row_idx, 24)

    #     self.case_rows = rows

    # def open_case(self, row, _):
    #     case_path = self.case_rows[row][5]
    #     self.case_window = CaseWindow(case_path)
    #     self.case_window.show()
