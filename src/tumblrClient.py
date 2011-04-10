#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from client import Client

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())
