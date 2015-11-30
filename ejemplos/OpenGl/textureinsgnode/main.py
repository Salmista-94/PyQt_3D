# -*- coding: utf-8 -*-
import os, sys, re

from PyQt5.QtNetwork import *

from fboinsgrenderer import *
from textureinsgnode_rc import *

from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import (QVariant, QUrl, QDir, QSortFilterProxyModel, pyqtProperty, QSize,
    Q_ENUMS, QObject, QRegExp, QAbstractItemModel, pyqtSignal, Qt, QModelIndex, QByteArray)
from PyQt5.QtQml import (QQmlApplicationEngine, QQmlEngine, QQmlFileSelector, qmlRegisterType,
    QQmlParserStatus, QJSValue)
from PyQt5.QtQuick import QQuickView, QQuickItem, QQuickWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    qmlRegisterType(FboInSGRenderer, "SceneGraphRendering", 1, 0, "Renderer")
    widgetWindow = QQuickView()
    widgetWindow.setResizeMode(QQuickView.SizeRootObjectToView)
    widgetWindow.setSource(QUrl("qrc:///main.qml"))
    widgetWindow.show()

    sys.exit(app.exec_())
