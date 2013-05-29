# -*- coding: utf-8 -*-

import sys
import logging
from configparser import SafeConfigParser

from PyQt4 import QtGui, QtOpenGL

from xivdm.dat.Manager import Manager as DatManager
from xivdm.logging_utils import set_logging

from xivdm.model.Model import Model

import OpenGL

OpenGL.FULL_LOGGING = True
import OpenGL.GL as gl
import OpenGL.GLU as glu
from OpenGL.GL import shaders

from OpenGL.GL.ARB import half_float_vertex

import ctypes

import numpy

class OpenGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, dat_manager):
        QtOpenGL.QGLWidget.__init__(self)
        self._dat_manager = dat_manager
        self._model = None

        self._vertex_vbo = None
        self._index_vbo = None

    def initializeGL(self):
        file_path = 'bg/ffxiv/fst_f1/fld/f1f1/bgparts/f1f1_a1_noko3.mdl'
        self._model = Model(file_path, self._dat_manager.get_file(file_path))

        gl.glClearColor(0,0,0,0)

        self._vertex_shader = shaders.compileShader("""#version 120
            in vec4 vPosition;

            void main()
            {
                gl_Position = gl_ModelViewProjectionMatrix * vPosition;
            }""", gl.GL_VERTEX_SHADER)

        self._fragment_shader = shaders.compileShader("""#version 120
            void main() 
            {
                gl_FragColor = vec4( 0, 1, 1, 1 );
            }""", gl.GL_FRAGMENT_SHADER)

        self._shader = shaders.compileProgram(self._vertex_shader, self._fragment_shader)
        gl.glBindAttribLocation(self._shader, 0, b"vPosition")

        # self._vertex_vbo = vbo.VBO(self._model._vertex_buffer, target=gl.GL_ARRAY_BUFFER)

        self._vertex_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_vbo)
        #l.glBufferData(gl.GL_ARRAY_BUFFER, self._model._vertex_buffer, gl.GL_STATIC_DRAW)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(self._model._vertex_buffer), self._model._vertex_buffer, gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)


        # self._index_vbo = vbo.VBO(self._model._index_buffer, target=gl.GL_ELEMENT_ARRAY_BUFFER)

        self._index_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_vbo)
        #gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self._model._index_buffer, gl.GL_STATIC_DRAW)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(self._model._index_buffer), self._model._index_buffer, gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        
    def resizeGL(self, w, h):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        #gl.glOrtho(-10, 10, -10, 10, -10, 10)
        gl.glOrtho(-1, 1, -1, 1, -1, 1)
        gl.glViewport(0, 0, w, h)

    def paintGL(self):
        # gl.glViewport(0, 0, self.width(), self.height())
        # gl.glClearColor(0.0, 1.0, 0.0, 1.0)
        # gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # gl.glColor3f(1.0, 0.0, 0.0)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        glu.gluPerspective(60.0, float(viewport[2])/float(viewport[3]), 0.1, 1000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(2.0, 2.0, 2.0,
          0.0, 0.0, 0.0,
          0.0, 1.0, 0.0)

        self.drawGrid(100)
        self.drawAxes()

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_INDEX_ARRAY)

        shaders.glUseProgram(self._shader)
        

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_vbo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_vbo)

        # self._vertex_vbo.bind()
        # self._index_vbo.bind()

        gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE)
        gl.glPolygonMode(gl.GL_BACK, gl.GL_LINE)

        for mesh in self._model._meshes:
        
            #mesh = self._model._meshes[0]

            #gl.glVertexAttribPointer(0, 4, gl.GL_FLOAT, False, 0, None)
            #gl.glVertexPointer(3, gl.GL_HALF_NV, False, None)
            gl.glVertexAttribPointer(0, 4, half_float_vertex.GL_HALF_FLOAT, False, mesh._vertex_size, ctypes.c_void_p(mesh._vertex_buffer_offset))
            gl.glEnableVertexAttribArray(0)
            
            #gl.glDrawElements(gl.GL_TRIANGLES, 18, gl.GL_UNSIGNED_SHORT, None)  mesh._index_count
            gl.glDrawElements(gl.GL_TRIANGLES, mesh._index_count, gl.GL_UNSIGNED_SHORT, ctypes.c_void_p(mesh._index_buffer_offset * 2))
            gl.glDisableVertexAttribArray(0)

        shaders.glUseProgram(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

        gl.glDisableClientState(gl.GL_INDEX_ARRAY)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        # gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_vbo)
        # gl.glVertexPointer(4, gl.GL_FLOAT, 0, None)
        # gl.glColor3f(1.0, 0.0, 0.0)
        # gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 3)
        # gl.glDisableVertexAttribArray(0)

        #shaders.glUseProgram(0)        

    def drawGrid(self, grid_size):
        grid_half_size = grid_size / 2
        gl.glBegin(gl.GL_LINES)
        gl.glColor3f(0.20, 0.20, 0.20)
        for i in range(grid_size):
            gl.glVertex3f(i - grid_half_size, -grid_half_size, 0)
            gl.glVertex3f(i - grid_half_size, grid_half_size, 0)
    
            gl.glVertex3f(-grid_half_size, i - grid_half_size, 0)
            gl.glVertex3f(grid_half_size, i - grid_half_size, 0)
        gl.glEnd()

    def drawAxes(self):
        gl.glLineWidth (2.0)
        gl.glBegin(gl.GL_LINES)

        gl.glColor3f(1,0,0)
        gl.glVertex3f(0,0,0)
        gl.glVertex3f(1,0,0)

        gl.glColor3f(0,1,0)
        gl.glVertex3f(0,0,0)
        gl.glVertex3f(0,1,0)

        gl.glColor3f(0,0,1)
        gl.glVertex3f(0,0,0)
        gl.glVertex3f(0,0,1)   

        gl.glEnd()
        gl.glLineWidth (1.0)

class SimpleTestWidget(QtOpenGL.QGLWidget):
    def __init__(self):
        QtOpenGL.QGLWidget.__init__(self)

    def initializeGL(self):
        self._vertexBuffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertexBuffer)
        vertices = numpy.array([0.5, 0.5, -0.5, 0.5, -0.5, -0.5, 0.5, -0.5], dtype='float32')
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices, gl.GL_STATIC_DRAW)    # Error

        self._indexBuffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._indexBuffer)
        indices = numpy.array([0, 1, 2, 2, 0, 3], dtype='uint32')
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices, gl.GL_STATIC_DRAW)    # Error

    def paintGL(self):
        gl.glViewport(0, 0, self.width(), self.height())
        gl.glClearColor(0.0, 1.0, 0.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glColor3f(1.0, 0.0, 0.0)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_INDEX_ARRAY)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertexBuffer)
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, None)
        
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._indexBuffer)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)

        gl.glDisableClientState(gl.GL_INDEX_ARRAY)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

def main():
    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmgui')

    dat_manager = DatManager(config.get('game', 'path'))

    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()
    main_window.setWindowTitle('Model Viewer')
 
    # main_window.setCentralWidget(SimpleTestWidget())
    main_window.setCentralWidget(OpenGLWidget(dat_manager))
    main_window.resize(640, 480)
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()