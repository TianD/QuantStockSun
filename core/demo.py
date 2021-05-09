import sys
import time

from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QGuiApplication
from PySide2.QtWidgets import QApplication, QLabel
from pyqt_screenshot.screenshot import Screenshot, constant

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    qtApp = QApplication(sys.argv)

    # main_window = QLabel()
    # img = Screenshot.take_screenshot(constant.CLIPBOARD)
    pos = Screenshot.take_screenshot_pos(constant.CLIPBOARD)
    print(pos)
    for i in range(10):
        screen = QGuiApplication.screens()[0]
        screenPixel = screen.grabWindow(0)
        img = screenPixel.copy(pos)
        print(img)
        img.save('e:/abc_%03d.jpg' % i )
        time.sleep(10)
    # main_window.show()
    # if img is not None:
    #     main_window.setPixmap(QPixmap(img))
    qtApp.exec_()
