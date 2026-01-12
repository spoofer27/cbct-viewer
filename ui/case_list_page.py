from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTableWidget, QTableWidgetItem
)
import sqlite3
from database.db import DB_PATH

class CaseListPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search case...")
        self.search.textChanged.connect(self.load_cases)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Age", "Gender", "Date"]
        )
        self.table.cellClicked.connect(self.open_case)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search)
        layout.addWidget(self.table)

        self.load_cases()

    def load_cases(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        rows = c.execute("""
        SELECT id, name, age, gender, date, path FROM cases
        """).fetchall()

        conn.close()

        self.rows = rows
        self.table.setRowCount(0)

        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for i in range(5):
                self.table.setItem(r, i, QTableWidgetItem(row[i]))

    def open_case(self, row, _):
        case_path = self.rows[row][5]
        self.main.open_case(case_path)
