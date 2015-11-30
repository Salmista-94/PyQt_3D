# -*- coding: utf-8 -*-
#from PyQt5.QtGui import QApplication
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QVariant, QUrl, QDir
from PyQt5.QtQml import QQmlApplicationEngine, QQmlEngine
from PyQt5.QtQuick import QQuickView, QQuickItem, QQuickWindow




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load(QUrl("qml/jsonmodels/jsonmodelsbasic.qml"))

    sys.exit(app.exec_())