import sys
import os
import time
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QScreen
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

dir_path = os.path.dirname(os.path.realpath(__file__))

app = QApplication([])


screen = app.primaryScreen()
screen_rect = screen.geometry()

window = QWidget()
window.setWindowTitle("Qt App")
window.setGeometry(100, 100, 280, 280)

window.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
pixmap = QPixmap(dir_path + '/lock.png')
pic = QLabel(parent = window)
pic.setPixmap(pixmap)
window.resize(pixmap.width(), pixmap.height())

window.move(screen_rect.right() - window.width(), screen_rect.top())

window.show()

sys.exit(app.exec())
