import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QPlainTextEdit
from PyQt5.QtCore import pyqtSlot
from numpy import arange, array
from math import *
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import Akima1DInterpolator


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self._data = []

        self._input = XPlainTextEdit(self)
        self._input.resize(240, 120)
        self._input.move(10, 10)

        plot_button = QPushButton('Go!', self)
        plot_button.move(150, 130)
        plot_button.clicked.connect(self.go)

        save_button = QPushButton('Log', self)
        save_button.move(10, 130)
        save_button.clicked.connect(self.log)

        self._input.setAcceptDrops(True)
        self.setFixedSize(261, 160)
        self.setWindowTitle('Akima\'s spline')
        self.setStyleSheet(open('style.css', 'r').read())
        self.show()

    @pyqtSlot()
    def go(self):
        try:
            y_data = list(map(lambda i: float(i), self.input.split(' ')))
        except ValueError:
            self.input = 'Invalid input!'
            return
        xs = array(range(0, len(y_data)))
        ys = array(y_data)
        sp = Akima1DInterpolator(xs, ys)
        spline = sp(arange(0, len(y_data), step=0.1))
        self.data = spline
        plt.close('all')
        plt.plot(spline, 'r-')
        plt.show()

    def log(self, data):
        if len(self.data) == 0:
            return
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        f = open('AkimasSplineLog%s.txt' % date, 'w')
        for yi in self.data:
            f.write('%f\n' % yi)
        f.close()

    @pyqtSlot()
    def import_txt(self):
        return

    @property
    def input(self):
        return self._input.toPlainText()

    @property
    def f_in(self):
        return self._f_in.text()

    @property
    def data(self):
        return self._data

    @input.setter
    def input(self, value):
        self._input.setPlainText(value)

    @data.setter
    def data(self, value):
        self._data = value


class XPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasText():
            contents = open(e.mimeData().text()[7:], 'r').read()
            self.setPlainText(contents)


app = QApplication(sys.argv)
gui = Window()
sys.exit(app.exec_())
