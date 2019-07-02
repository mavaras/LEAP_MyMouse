import math, sys
from PyQt4.QtCore import Qt, QTimer
from PyQt4.QtGui import *


class Overlay(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.exit = False

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))

        for c in range(6):
            if (self.counter/5) % 6 == c:
                painter.setBrush(QBrush(QColor("#04B97F")))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))

            painter.drawEllipse(
                (self.width() - self.width()/2) + 32*c - 90,
                (self.height() - 42),
                20, 20
            )

            """
            painter.drawEllipse(
                (self.width() - self.width()/5) + 30 * math.cos(2 * math.pi * i/6.0) - 10,
                (self.height() - self.height()/1.2) + 30 * math.sin(2 * math.pi * i/6.0) - 10,
                20, 20)
            """
        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(50)
        self.counter = 0

    def timerEvent(self, event):
        self.counter += 1
        self.update()
        if self.counter == 80:
            self.killTimer(self.timer)
            self.exit = True
            '''self.hide()
            self.parent().close()
            self.close()'''


class LoadScreen(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowOpacity(0)

        widget = QWidget(self)
        self.label = QLabel()
        self.label.setPixmap(QPixmap("res/logo.png"))
        self.label.show()
        layout = QGridLayout(widget)
        layout.addWidget(self.label, 0, 0, 1, 3)

        self.setCentralWidget(widget)
        self.overlay = Overlay(self.centralWidget())
        self.overlay.show()

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

    @staticmethod
    def _close():
        sys.exit()


"""
if __name__ == "__main__":
    app = QApplication([])
    ls = LoadScreen()
    ls.show()
    app.exec_()
"""
