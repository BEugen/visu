#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import mwindow
from PyQt5.QtWidgets import QApplication



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mwindow.visuDisp('0.0.0.0', 6500)
    sys.exit(app.exec_())
