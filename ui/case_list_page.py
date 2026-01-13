from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
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
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.cellClicked.connect(self.open_case)
        self.table.setSortingEnabled(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search)
        layout.addWidget(self.table)

        self.load_cases()

    def load_cases(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        search_text = self.search.text().strip()
        if search_text:
            query = """
            SELECT id, name, age, gender, date, path FROM cases
            WHERE name LIKE ? OR CAST(id AS TEXT) LIKE ? OR date LIKE ?
            """
            rows = c.execute(query, ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%')).fetchall()
        else:
            rows = c.execute("""
            SELECT id, name, age, gender, date, path FROM cases
            """).fetchall()

        conn.close()

    def load_cases(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        search_text = self.search.text().strip()
        if search_text:
            query = """
            SELECT id, name, age, gender, date, path FROM cases
            WHERE name LIKE ? OR CAST(id AS TEXT) LIKE ? OR date LIKE ?
            """
            rows = c.execute(query, ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%')).fetchall()
        else:
            rows = c.execute("""
            SELECT id, name, age, gender, date, path FROM cases
            """).fetchall()

        conn.close()

        self.rows = rows
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for i in range(5):
                val = row[i] if row[i] is not None else ""
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, i, item)

        self.table.setSortingEnabled(True)

    def open_case(self, row, _):
        case_path = self.rows[row][5]
        self.main.open_case(case_path)
