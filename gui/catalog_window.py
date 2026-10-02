# gui/catalog_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel, QMessageBox
from backend.dao import search_books

class CatalogWindow(QWidget):
    def __init__(self, user_id, role_id):
        super().__init__()
        self.user_id = user_id
        self.role_id = role_id
        self.setWindowTitle("SmartLibrary - Catalog")
        self.setGeometry(200,150,700,450)

        layout = QVBoxLayout()
        top = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title or author...")
        top.addWidget(self.search_input)
        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search)
        top.addWidget(self.search_btn)
        layout.addLayout(top)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.borrow_btn = QPushButton("Borrow Selected Book")
        self.borrow_btn.clicked.connect(self.borrow_selected)
        btn_layout.addWidget(self.borrow_btn)
        self.club_btn = QPushButton("Book Clubs")
        self.club_btn.clicked.connect(self.open_clubs)
        btn_layout.addWidget(self.club_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.search()

    def search(self):
        q = self.search_input.text().strip()
        rows = search_books(q)
        self.list_widget.clear()
        for r in rows:
            self.list_widget.addItem(f"{r['id']} | {r['title']} - {r['author']} (Available: {r['copies_available']})")

    def borrow_selected(self):
        sel = self.list_widget.currentItem()
        if not sel:
            QMessageBox.warning(self, "Error", "Select a book.")
            return
        book_id = int(sel.text().split("|")[0].strip())
        from gui.loan_window import LoanWindow
        self.loan_win = LoanWindow(self.user_id, book_id)
        self.loan_win.show()

    def open_clubs(self):
        from gui.club_window import ClubWindow
        self.club_win = ClubWindow()
        self.club_win.show()
