# -*- coding: utf-8 -*-
from logorenderer import *
from PyQt5.QtCore import Q_FLAGS
from PyQt5.QtGui import (QOpenGLFramebufferObject, QMatrix4x4, QVector3D, QOpenGLVertexArrayObject,
QOpenGLShader, QOpenGLShaderProgram, QOpenGLVersionProfile, QOpenGLContext, QOpenGLFramebufferObjectFormat)
from PyQt5.QtQuick import QQuickView, QQuickItem, QQuickWindow, QQuickFramebufferObject, QSGSimpleTextureNode
from PyQt5.QtWidgets import QApplication

class FboInSGRenderer(QQuickFramebufferObject):#<------------ 
    """docstring for FboInSGRenderer"""
    def __init__(self, parent= None):
        super(FboInSGRenderer, self).__init__(parent)
     
    def createRenderer(self):
        #print("FboInSGRenderer.createRenderer")
        logo = LogoInFboRenderer()
        return logo


class LogoInFboRenderer(QQuickFramebufferObject.Renderer):
    """docstring for LogoInFboRenderer"""
    def __init__(self):
        super(LogoInFboRenderer, self).__init__()
        self.logo = LogoRenderer()
        self.logo.initialize()
        self.frmBuffer = None
        #print("LogoInFboRenderer.__init__")

    def render(self):
        self.logo.render()
        self.update()

    def createFramebufferObject(self, size):
        #print("\n\nLogoInFboRenderer.createFramebufferObject", size)#, QApplication.instance()
        format = QOpenGLFramebufferObjectFormat()
        format.setAttachment(QOpenGLFramebufferObject.CombinedDepthStencil)
        format.setSamples(4)
        self.frmBuffer = QOpenGLFramebufferObject(size, format)
        #print("hola3", self.frmBuffer)
        return self.frmBuffer

    def framebufferObject(self):
        return self.frmBuffer

