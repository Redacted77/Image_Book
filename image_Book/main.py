import sys
from PySide6.QtWidgets import QApplication
from zoom_on_image import MainWindow

app = QApplication(sys.argv)
window = MainWindow(app)
window.show()
sys.exit(app.exec())