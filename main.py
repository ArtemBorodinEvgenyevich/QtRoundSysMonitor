from PySide2.QtWidgets import QApplication
from PySide2 import QtWidgets, QtCore, QtGui
from ram_widgets import RamDiagram
from cpu_widgets import CpuDiagram
from desktop_widget import desktop_widget
import sys, os
import platform

if platform.system() == 'Linux':
    # get current session id
    output = os.popen("loginctl").read().split("\n")
    print(output)
    a = output[1].split()
    print(a[0])
    # get a graphics server type
    # TODO: find an elegant way
    window_type = os.popen(f"loginctl show-session {output[1][9]} -p Type").read()
    print(window_type)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = desktop_widget()
    w.show()
    sys.exit(app.exec_())

