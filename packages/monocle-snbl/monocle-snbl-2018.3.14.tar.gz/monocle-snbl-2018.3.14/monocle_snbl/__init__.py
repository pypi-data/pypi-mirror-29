#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5 import QtWidgets
from .controller import Controller


app = None


def main():
    logging.basicConfig(level=logging.DEBUG)
    global app
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('monocle')
    ctrl = Controller()
    ctrl.start()
    sys.exit(app.exec())
