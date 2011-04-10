#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, uic

class Credentials(QtGui.QDialog):
    def __init__(self, *args):
        super(Credentials, self).__init__(*args)
        uic.loadUi("credentials.ui", self)
