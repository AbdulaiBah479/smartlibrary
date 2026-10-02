# gui/loan_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from backend.dao import get_member_by_user_id, count_active_loans, borrow_book

class LoanWindow(QWidget):
    def __init__(self, user_id, book_id):
        super().__init__()
        self.user_id = user_id
        self.book_id = book_id
        self.setWindowTitle("Borrow Book")
        self.setGeometry(350,250,320,180)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Book ID: {book_id}"))

        member = get_member_by_user_id(self.user_id)
        if not member:
            layout.addWidget(QLabel("You are not a registered member."))
            self.member_id = None
        else:
            self.member_id = member['id']
            active = count_active_loans(self.member_id)
            layout.addWidget(QLabel(f"Active loans: {active} / 3"))

        self.borrow_btn = QPushButton("Confirm Borrow")
        self.borrow_btn.clicked.connect(self.confirm)
        layout.addWidget(self.borrow_btn)
        self.setLayout(layout)

    def confirm(self):
        if not self.member_id:
            QMessageBox.warning(self, "Error", "You must be a member.")
            return
        try:
            loan_id = borrow_book(self.member_id, self.book_id)
            QMessageBox.information(self, "Success", f"Loan created: {loan_id}")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
