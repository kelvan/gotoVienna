#!/usr/bin/env python

import sys
import os.path
import webbrowser
from PySide.QtCore import SIGNAL, QTranslator, QObject
from PySide.QtGui import QApplication, QMainWindow
from Ui_Qt import Ui_MainWindow
from wlSearch import Search
from history import History
import settings


class WienerLinienQt(QMainWindow, Ui_MainWindow):
    types = ('stop', 'address', 'poi')

    def __init__(self):
        QMainWindow.__init__(self)
        # _s is used to keep a reference to the Search object, so it does
        # not get destroyed when it falls out of scope (the QML view is
        # destroyed as soon as the Search object is destroyed!)
        self._s = None
        self.setupUi(self)
        self.connect(self.btnSearch, SIGNAL("clicked()"), self.search)
        self.connect(self.actionToggle, SIGNAL("activated()"), self.toggle)

        self.history = History(settings.hist_file)
        self.editOrigin.addItems(self.history)
        self.editDestination.addItems(self.history)

        self.editOrigin.clearEditText()
        self.editDestination.clearEditText()

    def search(self):
        origin = self.editOrigin.currentText()
        destination = self.editDestination.currentText()

        if not (origin and destination):
            self.btnSearch.setText(self.btnSearch.tr("Search - Missing input"))
            return False

        self.history.insert(0, origin)
        self.history.insert(0, destination)

        if not origin in self.history:
            self.editOrigin.insertItems(0, origin)
            self.editDestination.insertItems(0, origin)

        if not destination in self.history:
            self.editOrigin.insertItems(0, destination)
            self.editDestination.insertItems(0, destination)

        self._s = Search(origin, destination, \
                   origin_type=self.types[self.comboOrigin.currentIndex()], \
                   destination_type=self.types[self.comboDestination.currentIndex()])
        self._s.open_qml()
        return True

    def toggle(self):
        eo = self.editOrigin.currentText()
        ed = self.editDestination.currentText()
        self.editOrigin.setEditText(ed)
        self.editDestination.setEditText(eo)

        co = self.comboOrigin.currentIndex()
        cd = self.comboDestination.currentIndex()
        self.comboOrigin.setCurrentIndex(cd)
        self.comboDestination.setCurrentIndex(co)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    t = QTranslator()
    t.load('', directory='lang', suffix='po')
    app.installTranslator(t)
    w = WienerLinienQt()
    w.show()
    sys.exit(app.exec_())
