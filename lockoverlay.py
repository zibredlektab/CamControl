import sys
import os
import time
import subprocess
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QEvent
from PyQt6.QtGui import QPixmap, QScreen, QKeyEvent
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QDialog, QMainWindow

dir_path = os.path.dirname(os.path.realpath(__file__))

enable = 'xinput enable 8'
disable = 'xinput disable 8'

time_to_shutdown = 5
time_countdown_began = 0

class LockIcon(QWidget):
    def __init__(self):
        super().__init__(parent = None)
        self.setGeometry(100, 100, 400, 280)
        
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        pixmap = QPixmap(dir_path + '/lock.png')
        pic = QLabel(parent = self)
        pic.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())        
        screen = app.primaryScreen()
        screen_rect = screen.geometry()
        self.move(screen_rect.right() - self.width(), screen_rect.top())
        
        print('Lock icon is displayed')
    
    def keyPressEvent(self, event):
        super(LockIcon, self).keyPressEvent(event)
        print('Enabling input')
        subprocess.call(enable, shell=True)
        exit()
        
class ShutDownWarning(QMainWindow):
    def __init__(self):
    
        time_to_shutdown = 5
        time_countdown_began = 0
        super().__init__(parent = None)
        self.setGeometry(100, 400, 400, 280)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        warning = QLabel("Shutdown in " + str(time_to_shutdown) + "...")
        self.setCentralWidget(warning)
        time_countdown_began = time.monotonic()
    
    def keyPressEvent(self, event):
        super(ShutDownWarning, self).keyPressEvent(event)
        print('Key is still down')
        if time.monotonic() - time_countdown_began > 1:
            print("hi")
        if time_to_shutdown <= 0:
            exit()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    lock = LockIcon()
    lock.show()
    
    print ('Disabling input')
    #subprocess.call(disable, shell=True)
    
    sys.exit(app.exec())