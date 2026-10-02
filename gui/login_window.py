# gui/login_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from backend.dao import get_user_by_username, create_user, create_member

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartLibrary - Login")
        self.setGeometry(300,200,320,220)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        self.username = QLineEdit()
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.do_login)
        layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Register (Member)")
        self.register_btn.clicked.connect(self.do_register)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def do_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter username and password.")
            return
        user = get_user_by_username(username)
        if not user:
            QMessageBox.warning(self, "Error", "User not found.")
            return
        from backend.dao import check_password
        if check_password(password, user['password_hash']):
            QMessageBox.information(self, "Welcome", f"Welcome {username}")
            from gui.catalog_window import CatalogWindow
            self.catalog = CatalogWindow(user['id'], user['role_id'])
            self.catalog.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Incorrect password.")

    def do_register(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter username and password.")
            return
        try:
            user_id = create_user(username, password, role_id=2)
            create_member(user_id, username, membership_no=f"M-{user_id:04d}")
            QMessageBox.information(self, "Success", "Member account created.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
