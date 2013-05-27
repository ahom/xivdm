# -*- coding: utf-8 -*-

import sys
import logging
from configparser import SafeConfigParser

from PySide import QtGui, QtOpenGL

from xivdm.dat.Manager import Manager as DatManager
from xivdm.logging_utils import set_logging

from xivdm.model.Model import Model

import OpenGL.GL as gl
from OpenGL.GL import shaders

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

        self._vertex_shader = shaders.compileShader(b"#version 330\nattribute vec4 vPosition;\nvoid main()\n{gl_Position = vPosition;}", gl.GL_VERTEX_SHADER)

        self._fragment_shader = shaders.compileShader("""#version 330
            void main() 
            {
                gl_FragColor = vec4( 0, 1, 0, 1 );
            }""", gl.GL_FRAGMENT_SHADER)

        self._shader = shaders.compileProgram(self._vertex_shader, self._fragment_shader)

        self._vertex_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_vbo);
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(self._model._vertex_buffer), self._model._vertex_buffer, gl.GL_STATIC_DRAW);

        self._index_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_vbo);
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(self._model._index_buffer), self._model._index_buffer, gl.GL_STATIC_DRAW);

    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are (-+1, -+1)
        gl.glOrtho(-20, 20, -20, 20, -20, 20)

    def paintGL(self):
        shaders.glUseProgram(self._shader)

        mesh = self._model._meshes[0]

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_vbo);
        gl.glEnableVertexAttribArray(0);
        gl.glVertexAttribPointer(0, 4, gl.GL_HALF_NV, False, mesh._vertex_size - 8, mesh._vertex_buffer_offset);
     
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._index_vbo);
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