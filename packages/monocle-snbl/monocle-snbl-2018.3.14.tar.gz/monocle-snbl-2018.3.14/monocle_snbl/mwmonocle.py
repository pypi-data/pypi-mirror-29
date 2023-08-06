#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
from .ui.ui_mwmonocle import Ui_MWMonocle


class MWMonocle(QtWidgets.QMainWindow, Ui_MWMonocle):
    sigClose = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.chunkSize = 200
        self.maxChunks = 10
        self.curves = [[], [], [], []]
        self.data = [
            np.empty((self.chunkSize + 1, 2)),
            np.empty((self.chunkSize + 1, 2)),
            np.empty((self.chunkSize + 1, 2)),
            np.empty((self.chunkSize + 1, 2)),
        ]
        self.ptr = [0, 0, 0, 0]
        self.startTime = pg.ptime.time()
        self.setUI()

    def setUI(self):
        self.setupUi(self)
        self.plots = [
            self.plot0.addPlot(),
            self.plot1.addPlot(),
            self.plot2.addPlot(),
            self.plot3.addPlot(),
        ]
        for p in self.plots:
            p.setLabel('bottom', 'Time', 's')
            p.setLabel('left', 'T', 'C')
            p.setXRange(-60, 0)
            p.setYRange(18, 35)

    def saveSettings(self):
        s = QtCore.QSettings().setValue
        s('MWMonocle/Geometry', self.saveGeometry())
        s('MWMonocle/State', self.saveState())

    def loadSettings(self):
        s = QtCore.QSettings().value
        self.restoreGeometry(s('MWMonocle/Geometry', b''))
        self.restoreState(s('MWMonocle/State', b''))

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.sigClose.emit()
        super().closeEvent(event)

    def setValue(self, sensor: int, value: float):
        label = getattr(self, f'labelT{sensor}', None)
        if not label:
            return
        label.setText(f'Temperature: {value:.1f} C')
        self.drawCurve(sensor, value)

    def drawCurve(self, sensor: int, value: float):
        now = pg.ptime.time()
        for c in self.curves[sensor]:
            c.setPos(-(now - self.startTime), 0)
        i = self.ptr[sensor] % self.chunkSize
        if i == 0:
            curve = self.plots[sensor].plot()
            self.curves[sensor].append(curve)
            last = self.data[sensor][-1] if self.ptr[sensor] != 0 else value
            self.data[sensor] = np.empty((self.chunkSize + 1, 2))
            self.data[sensor][0] = last
            while len(self.curves[sensor]) > self.maxChunks:
                c = self.curves[sensor].pop(0)
                self.plots[sensor].removeItem(c)
        else:
            curve = self.curves[sensor][-1]
        self.data[sensor][i + 1, 0] = now - self.startTime
        self.data[sensor][i + 1, 1] = value
        curve.setData(x=self.data[sensor][:i + 2, 0], y=self.data[sensor][:i + 2, 1], pen=pg.mkPen(width=3, color='r'))
        self.ptr[sensor] += 1
        self.plots[sensor].setXRange(-60, 0)
