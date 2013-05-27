# -*- coding: utf-8 -*-

import sys
import logging
from configparser import SafeConfigParser

from PyQt4 import QtGui, QtOpenGL

from xivdm.dat.Manager import Manager as DatManager
from xivdm.logging_utils import set_logging

from xivdm.model.Model import Model

import OpenGL

import OpenGL.GL as gl

from OpenGL.GL import shaders

OpenGL.FULL_LOGGING = True

import OpenGL.arrays.vbo as glvbo

class OpenGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, dat_manager):
        QtOpenGL.QGLWidget.__init__(self)
        self._dat_manager = dat_manager
        self._model = None

        self._vertex_vbo = None
        self._index_vbo = None

    def initializeGL(self):
        file_path = 'chara/monster/m0104/obj/body/b0001/model/m0104b0001.mdl'
        self._model = Model(file_path, self._dat_manager.get_file(file_path))

        gl.glClearColor(0,0,0,0)

        self._vertex_vbo = glvbo.VBO(self._model._vertex_buffer, usage=gl.GL_STATIC_DRAW)
        self._index_vbo = glvbo.VBO(self._model._index_buffer, usage=gl.GL_STATIC_DRAW, target=gl.GL_ELEMENT_ARRAY_BUFFER)

    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(-1, 1, -1, 1, -1, 1)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glColor(1,1,0)            

        for mesh in self._model._meshes:
            self._vertex_vbo.bind()
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            gl.glVertexPointer(4, gl.GL_HALF_FLOAT, mesh._vertex_size - 8, mesh._vertex_buffer_offset)

            self._index_vbo.bind()
            gl.glEnableClientState(gl.GL_INDEX_ARRAY)
            gl.glDrawElements(gl.GL_TRIANGLES, mesh._index_count, gl.GL_UNSIGNED_SHORT, mesh._index_buffer_offset);

def main():
    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmgui')

    dat_manager = DatManager(config.get('game', 'path'))

    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()
    main_window.setWindowTitle('Model Viewer')
 
    main_window.setCentralWidget(OpenGLWidget(dat_manager))
    main_window.resize(640, 480)
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()