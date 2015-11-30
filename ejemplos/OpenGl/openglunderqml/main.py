# -*- coding: utf-8 -*-
import os, sys, array

from PyQt5.QtGui import (QSurfaceFormat, QOpenGLShaderProgram, QOpenGLContext,
    QOpenGLVersionProfile, QOpenGLShader, QGuiApplication)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QVariant, QUrl, QDir, pyqtProperty, pyqtSignal, pyqtSlot, QSize, Qt, QObject
from PyQt5.QtQml import QQmlApplicationEngine, QQmlEngine, QQmlFileSelector
from PyQt5.QtQuick import QQuickView, QQuickItem, QQuickWindow

from PyQt5.QtQml import (qmlAttachedPropertiesObject, qmlRegisterType,
        QQmlComponent, QQmlEngine, QQmlListProperty)
from PyQt5.QtTest import QTest



class SquircleRenderer(QObject):#QOpenGLFunctions
    """docstring for SquircleRenderer"""
    def __init__(self, parent= None):
        super(SquircleRenderer, self).__init__(parent)
        self.m_t = 0.0
        self.m_program = None
        self.m_viewportSize = QSize()



    def setT(self, t):
        self.m_t = t

    def setViewportSize(self, size):
        self.m_viewportSize = size

    def setWin(self, win):
        self.win = win

        ver = QOpenGLVersionProfile()
        ver.setVersion(2, 1)

        self.m_context = self.win.openglContext()
        self.gl = self.m_context.versionFunctions(ver)



    @pyqtSlot()
    def paint(self):
        if not self.m_program:
            self.gl.initializeOpenGLFunctions()

            self.m_program = QOpenGLShaderProgram(self)
            self.m_program.addShaderFromSourceCode(QOpenGLShader.Vertex,
                                               "attribute highp vec4 vertices;"
                                               "varying highp vec2 coords;"
                                               "void main() {"
                                               "    gl_Position = vertices;"
                                               "    coords = vertices.xy;"
                                               "}")
            self.m_program.addShaderFromSourceCode(QOpenGLShader.Fragment,
                                               "uniform lowp float t;"
                                               "varying highp vec2 coords;"
                                               "void main() {"
                                               "    lowp float i = 1. - (pow(abs(coords.x), 4.) + pow(abs(coords.y), 4.));"
                                               "    i = smoothstep(t - 0.8, t + 0.8, i);"
                                               "    i = floor(i * 20.) / 20.;"
                                               "    gl_FragColor = vec4(coords * .5 + .5, i, i);"
                                               "}")


            self.m_program.bindAttributeLocation("vertices", 0)
            
            self.m_program.link()
        


        self.m_program.bind()


        self.m_program.enableAttributeArray(0)
 

        values = [(-1, -1),
                  (1, -1),
                  (-1, 1),
                  (1, 1) ]
        


        self.m_program.setAttributeArray(0, values)

        self.m_program.setUniformValue("t", self.m_t)
 

        #print("DATA:",self.m_viewportSize.width(), self.m_viewportSize.height(), self.m_t)#, self.gl.glViewport)

        self.gl.glViewport(0, 0, self.m_viewportSize.width(), self.m_viewportSize.height())

        self.gl.glDisable(self.gl.GL_DEPTH_TEST)


        self.gl.glClearColor(0, 0, 0, 1)
  
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)

  
        self.gl.glEnable(self.gl.GL_BLEND)
  
        self.gl.glBlendFunc(self.gl.GL_SRC_ALPHA, self.gl.GL_ONE)

 
        self.gl.glDrawArrays(self.gl.GL_TRIANGLE_STRIP, 0, 4)

  
        self.m_program.disableAttributeArray(0)

        self.m_program.release()





class Squircle(QQuickItem):
    """docstring for Squircle"""
    tChanged = pyqtSignal()
    
    @pyqtProperty(float, notify=tChanged)
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        if value == self._t:
            return
        self._t = value
        self.tChanged.emit()

        if self.window():
            self.window().update()

    def __init__(self, arg):
        super(Squircle, self).__init__()
        self._t = 0.0
        self.m_renderer = None
        self.windowChanged['QQuickWindow*'].connect(self.handleWindowChanged)


    @pyqtSlot()
    def cleanup(self):
        if self.m_renderer:
            print("cleanup.....................")
            self.m_renderer = None
    
    @pyqtSlot()
    def sync(self):
        if not self.m_renderer:
            print("sync<----------------")
            self.m_renderer = SquircleRenderer()#self.window())
            self.window().beforeRendering.connect(self.m_renderer.paint, Qt.DirectConnection)

        self.m_renderer.setViewportSize(self.window().size() * self.window().devicePixelRatio())
        self.m_renderer.setT(self._t)
        self.m_renderer.setWin(self.window())
    
    
    #@pyqtSlot(QQuickWindow)
    def handleWindowChanged(self, win):
        if win:
            win.beforeSynchronizing.connect(self.sync, Qt.DirectConnection)
            win.sceneGraphInvalidated.connect(self.cleanup, Qt.DirectConnection)
    
            win.setClearBeforeRendering(False)
    

    












if __name__ == '__main__':
    app = QApplication(sys.argv)

    qmlRegisterType(Squircle, "OpenGLUnderQML", 1, 0, "Squircle")
    viewer = QQuickView(QUrl.fromLocalFile("main.qml"))

    viewer.show()

    sys.exit(app.exec_())