# -*- coding: utf-8 -*-
import math

from PyQt5.QtCore import Q_FLAGS
from PyQt5.QtGui import (QOpenGLFramebufferObject, QMatrix4x4, QVector3D, QOpenGLVertexArrayObject,
QOpenGLShader, QOpenGLShaderProgram, QOpenGLVersionProfile, QOpenGLContext)
from PyQt5._QOpenGLFunctions_2_1 import QOpenGLFunctions_2_1



class LogoRenderer():#protected QOpenGLFunctions
    """docstring for LogoRenderer"""
    def __init__(self):
        super(LogoRenderer, self).__init__()
        self.m_fAngle = None
        self.m_fScale = None
        self.vertices = []
        self.normals = []
        self.program1 = QOpenGLShaderProgram()
        self.vertexAttr1 = 0
        self.normalAttr1 = 0
        self.matrixUniform1 = 0

        ver = QOpenGLVersionProfile()
        ver.setVersion(2, 1)
        cntx = QOpenGLContext.currentContext()
        #print("QOpenGLContext:", cntx, ver)
        fmt = cntx.format()
        fmt.setVersion(2, 1)
        cntx.setFormat(fmt)
        self.gl = cntx.versionFunctions(ver)


    def render(self):
        self.gl.glDepthMask(True)

        self.gl.glClearColor(0.5, 0.5, 0.7, 1.0)
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)

        self.gl.glTexParameteri(self.gl.GL_TEXTURE_2D, self.gl.GL_TEXTURE_MIN_FILTER, self.gl.GL_LINEAR )
        self.gl.glTexParameteri(self.gl.GL_TEXTURE_2D, self.gl.GL_TEXTURE_MAG_FILTER, self.gl.GL_LINEAR )

        self.gl.glFrontFace(self.gl.GL_CW)
        self.gl.glCullFace(self.gl.GL_FRONT)
        self.gl.glEnable(self.gl.GL_CULL_FACE)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)

        modelview = QMatrix4x4()
        modelview.rotate(self.m_fAngle, 0.0, 1.0, 0.0)
        modelview.rotate(self.m_fAngle, 1.0, 0.0, 0.0)
        modelview.rotate(self.m_fAngle, 0.0, 0.0, 1.0)
        modelview.scale(self.m_fScale)
        modelview.translate(0.0, -0.2, 0.0)

        self.program1.bind()
        self.program1.setUniformValue(self.matrixUniform1, modelview)
        self.paintQtLogo()
        self.program1.release()

        self.gl.glDisable(self.gl.GL_DEPTH_TEST)
        self.gl.glDisable(self.gl.GL_CULL_FACE)

        self.m_fAngle += 1.0

    def initialize(self):
        #print("initialize.gls")
        self.gl.initializeOpenGLFunctions()

        self.gl.glClearColor(0.1, 0.1, 0.2, 1.0)

        vshader1 = QOpenGLShader(QOpenGLShader.Vertex, self.program1)
        vsrc1 = str("attribute highp vec4 vertex;\n"
                "attribute mediump vec3 normal;\n"
                "uniform mediump mat4 matrix;\n"
                "varying mediump vec4 color;\n"
                "void main(void)\n"
                "{\n"
                "    vec3 toLight = normalize(vec3(0.0, 0.3, 1.0));\n"
                "    float angle = max(dot(normal, toLight), 0.0);\n"
                "    vec3 col = vec3(0.40, 1.0, 0.0);\n"
                "    color = vec4(col * 0.2 + col * 0.8 * angle, 1.0);\n"
                "    color = clamp(color, 0.0, 1.0);\n"
                "    gl_Position = matrix * vertex;\n"
                "}\n")
        vshader1.compileSourceCode(vsrc1)

        fshader1 = QOpenGLShader(QOpenGLShader.Fragment, self.program1)
        fsrc1 = str("varying mediump vec4 color;\n"
                "void main(void)\n"
                "{\n"
                "    gl_FragColor = color;\n"
                "}\n")
        fshader1.compileSourceCode(fsrc1)

        self.program1.addShader(vshader1)
        self.program1.addShader(fshader1)
        self.program1.link()

        self.vertexAttr1 = self.program1.attributeLocation("vertex")
        self.normalAttr1 = self.program1.attributeLocation("normal")
        self.matrixUniform1 = self.program1.uniformLocation("matrix")

        self.gl.glTexParameteri(self.gl.GL_TEXTURE_2D, self.gl.GL_TEXTURE_MIN_FILTER, self.gl.GL_LINEAR )
        self.gl.glTexParameteri(self.gl.GL_TEXTURE_2D, self.gl.GL_TEXTURE_MAG_FILTER, self.gl.GL_LINEAR )

        self.m_fAngle = 0
        self.m_fScale = 1
        self.createGeometry()

    def paintQtLogo(self):
        self.program1.enableAttributeArray(self.normalAttr1)
        self.program1.enableAttributeArray(self.vertexAttr1)
        self.program1.setAttributeArray(self.vertexAttr1, self.vertices)
        self.program1.setAttributeArray(self.normalAttr1, self.normals)
        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, len(self.vertices))
        self.program1.disableAttributeArray(self.normalAttr1)
        self.program1.disableAttributeArray(self.vertexAttr1)

    def createGeometry(self):
        self.vertices.clear()
        self.normals.clear()

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        NumSectors = 100

        for i in range(NumSectors):
            angle1 = (i * 2 * math.pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * math.pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)
        

        for i in range(len(self.vertices)):
            self.vertices[i] *= 2.0



    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        #print("quad inicio")
        self.vertices.append(QVector3D(x1, y1, -0.05))
        self.vertices.append(QVector3D(x2, y2, -0.05))
        self.vertices.append(QVector3D(x4, y4, -0.05))

        self.vertices.append(QVector3D(x3, y3, -0.05))
        self.vertices.append(QVector3D(x4, y4, -0.05))
        self.vertices.append(QVector3D(x2, y2, -0.05))

        n = QVector3D.normal(QVector3D(x2 - x1, y2 - y1, 0.0), QVector3D(x4 - x1, y4 - y1, 0.0))

        for i in range(6):
            self.normals.append(n)

        self.vertices.append(QVector3D(x4, y4, 0.05))
        self.vertices.append(QVector3D(x2, y2, 0.05))
        self.vertices.append(QVector3D(x1, y1, 0.05))

        self.vertices.append(QVector3D(x2, y2, 0.05))
        self.vertices.append(QVector3D(x4, y4, 0.05))
        self.vertices.append(QVector3D(x3, y3, 0.05))

        n = QVector3D.normal(QVector3D(x2 - x4, y2 - y4, 0.0), QVector3D(x1 - x4, y1 - y4, 0.0))

        for i in range(6):
            self.normals.append(n)
        #print("quad fin")

    def extrude(self, x1, y1, x2, y2):
        #print("extrude inicio")
        self.vertices.append(QVector3D(x1, y1, +0.05))
        self.vertices.append(QVector3D(x2, y2, +0.05))
        self.vertices.append(QVector3D(x1, y1, -0.05))

        self.vertices.append(QVector3D(x2, y2, -0.05))
        self.vertices.append(QVector3D(x1, y1, -0.05))
        self.vertices.append(QVector3D(x2, y2, +0.05))

        n = QVector3D.normal(QVector3D(x2 - x1, y2 - y1, 0.0), QVector3D(0.0, 0.0, -0.1))

        for i in range(6):
            self.normals.append(n)
        #print("extrude fin")


