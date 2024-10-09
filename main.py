import sys
from PyQt5.QtWidgets import QApplication
from ui import TelegramApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelegramApp()
    window.show()
    sys.exit(app.exec_())
