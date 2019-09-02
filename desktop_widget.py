from PySide2 import QtWidgets, QtGui, QtCore
from cpu_widgets import CpuDiagram
from ram_widgets import RamDiagram
import sys


class desktop_widget(QtWidgets.QWidget):
    def __init__(self):
        super(desktop_widget, self).__init__()
        self.setFixedSize(372, 222)

        cpu = CpuDiagram()
        ram = RamDiagram()

        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(0)

        hbox.addWidget(cpu, alignment=QtCore.Qt.AlignCenter)
        hbox.addWidget(ram, alignment=QtCore.Qt.AlignBottom)

        self.setLayout(hbox)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.Tool
                            #QtCore.Qt.WindowStaysOnBottomHint
                            )

    def mousePressEvent(self, event:QtGui.QMouseEvent):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event:QtGui.QMouseEvent):
        teta = QtCore.QPoint(event.globalPos() - self.old_pos)
        self.move(self.x() + teta.x(), self.y() + teta.y())
        self.old_pos = event.globalPos()

