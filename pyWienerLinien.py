#!/usr/bin/env python

import sys
import os
import time
import logging
from PySide import QtCore, QtGui
from Ui_Qt import Ui_MainWindow
from wlSearch import Search
import webbrowser


class WienerLinienQt(QtGui.QMainWindow, Ui_MainWindow):
    types = ('stop', 'address', 'poi')

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.connect(self.btnSearch, QtCore.SIGNAL("clicked()"), self.search)

    def search(self):
        origin = self.editOrigin.currentText()
        destination = self.editDestination.currentText()
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
