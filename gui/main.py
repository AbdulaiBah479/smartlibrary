# gui/main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
