from PySide2 import QtWidgets, QtCore, QtGui
from psutil import cpu_percent


class CpuDiagram(QtWidgets.QWidget):
    percentChanged = QtCore.Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)

        # color constants
        self.dark = "#3B3A44"
        self.light = "#4A4953"
        self.color = "#75ECB5"

        # text constants
        self.module_name = "CPU"
        self.postfix = "average"

        # timer with an interval of 1 sec
        self.timer = QtCore.QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start()

        # animation initialization
        self._percent = 0
        self._animation = QtCore.QPropertyAnimation(self, b"percent", duration=400)
        self._animation.setEasingCurve(QtCore.QEasingCurve.OutExpo)

        self.percentChanged.connect(self.update)

        #self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)



    @QtCore.Slot()
    def onTimeout(self):
        start_value = self.percent
        end_value = cpu_percent()

        self._animation.setStartValue(start_value)
        self._animation.setEndValue(end_value)
        self._animation.setDuration(1000)
        self._animation.start()

    def get_percent(self):
        return self._percent

    def set_percent(self, p):
        if self._percent != p:
            self._percent = p
            self.percentChanged.emit(p)

    percent = QtCore.Property(
        float, fget=get_percent, fset=set_percent, notify=percentChanged
    )

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # draw base
        basic_rect = self.rect().adjusted(5, 5, -5, -5)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(self.dark)))
        painter.drawEllipse(basic_rect)

        # draw arc
        pen = QtGui.QPen(QtGui.QColor(self.light))
        pen.setWidth(10)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen)
        arc_rect = basic_rect.adjusted(15, 15, -15, -15)
        painter.drawEllipse(arc_rect)

        # draw active arc
        pen.setColor(QtGui.QColor(self.color))
        start_angle = 90
        span_angle = self.percent_to_angle(self.percent)
        painter.setPen(pen)
        painter.drawArc(arc_rect, start_angle * 16, span_angle * 16)

        # draw text

        # draw module name
        painter.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.white)))
        font = QtGui.QFont()
        font.setPixelSize(50)
        painter.setFont(font)
        arc_rect.moveTop(0)
        painter.drawText(arc_rect, QtCore.Qt.AlignCenter, self.module_name)

        # draw postfix
        font = QtGui.QFont()
        font.setPixelSize(22)
        painter.setFont(font)
        arc_rect.moveTop(-30)
        painter.drawText(
            arc_rect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, self.postfix
        )

        # draw percents
        font = QtGui.QFont()
        font.setPixelSize(18)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(self.color))
        arc_rect.moveTop(0)
        painter.drawText(
            arc_rect,
            QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom,
            f"{self.percent:.2f} %",
        )

    def percent_to_angle(self, percent):
        return -percent / 100 * 360

