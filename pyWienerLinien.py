#!/usr/bin/env python

import sys
import os
import time
import logging
import webbrowser
from PySide import QtCore, QtGui
from Ui_Qt import Ui_MainWindow
from wlSearch import Search
from history import History
import settings


class WienerLinienQt(QtGui.QMainWindow, Ui_MainWindow):
    types = ('stop', 'address', 'poi')

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.connect(self.btnSearch, QtCore.SIGNAL("clicked()"), self.search)

        self.history = History(settings.hist_file)
        self.editOrigin.addItems(self.history)
        self.editDestination.addItems(self.history)

    def search(self):
        origin = self.editOrigin.currentText()
        destination = self.editDestination.currentText()

        self.history.insert(0, origin)
        self.history.insert(0, destination)

        self.editOrigin.insertItems(1, self.history)
        self.editDestination.insertItems(1, self.history)

        if not origin and destination:
            self.btnSearch.setText("Search - Missing input")
        else:
            s = Search(origin, destination, \
                       origin_type=self.types[self.comboOrigin.currentIndex()], \
                       destination_type=self.types[self.comboDestination.currentIndex()])
            try:
                s.open_browser()
            except webbrowser.Error:
                self.btnSearch.setText("Error starting webbrowser")
                return False
            self.btnSearch.setText("Search - Opening webbrowser")
            return True


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = WienerLinienQt()
    w.show()
    app.exec_()
