# gui/club_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
from backend.db import get_connection

class ClubWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Clubs")
        self.setGeometry(350,250,420,320)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Club name:"))
        self.club_input = QLineEdit()
        layout.addWidget(self.club_input)
        self.create_btn = QPushButton("Create Club")
        self.create_btn.clicked.connect(self.create_club)
        layout.addWidget(self.create_btn)
        layout.addWidget(QLabel("Clubs:"))
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.load_clubs()

    def create_club(self):
        name = self.club_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Enter name")
            return
        conn = get_connection()
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO book_clubs (name) VALUES (%s)", (name,))
                    conn.commit()
            QMessageBox.information(self, "Success", "Club created.")
            self.club_input.clear()
            self.load_clubs()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        finally:
            conn.close()

    def load_clubs(self):
        self.list_widget.clear()
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM book_clubs ORDER BY id ASC")
                rows = cur.fetchall()
                for r in rows:
                    self.list_widget.addItem(f"{r[0]} | {r[1]}")
        finally:
            conn.close()
