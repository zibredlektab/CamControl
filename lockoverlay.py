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


class Window(QWidget):
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
        super(Window, self).keyPressEvent(event)
        print('Enabling input')
        subprocess.call(enable, shell=True)
        exit()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Window()
    window.show()
    
    print ('Disabling input')
    subprocess.call(disable, shell=True)
    
    sys.exit(app.exec())