#!/usr/bin/python
# -*- coding: utf-8 -*-

# simple.py

import sys
from PySide import QtGui

app = QtGui.QApplication(sys.argv)
idx = QtGui.QApplication.desktop().primaryScreen()
print QtGui.QApplication.desktop().availableGeometry()
print QtGui.QApplication.desktop().screen(1).rect()

wid = QtGui.QWidget()
wid.resize(250, 150)
wid.setWindowTitle('Simple')
wid.show()

sys.exit(app.exec_())
