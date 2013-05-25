# -*- coding: utf-8 -*-

import sys
import logging
from configparser import SafeConfigParser

from PyQt4 import QtGui, QtOpenGL

from xivdm.dat.Manager import Manager as DatManager
from xivdm.logging_utils import set_logging

from xivdm.model.Model import Model


class OpenGLWidget(QtOpenGL.QGLWidget):
    def __init__(self, dat_manager):
        QtOpenGL.QGLWidget.__init__(self)
        self._dat_manager = dat_manager
        self._model = None

        self._vertex_buffers = []
        self._index_buffers = []


    def initializeGL(self):
        file_path = 'chara/monster/m0104/obj/body/b0001/model/m0104b0001.mdl'
        self._model = Model(file_path, self._dat_manager.get_file(file_path))

        for buffer_object in self._model._buffer_objects:
            vertex_buffer = QtOpenGL.QGLBuffer(QtOpenGL.QGLBuffer.VertexBuffer)
            vertex_buffer.create();
            vertex_buffer.bind();
            vertex_buffer.setUsagePattern(QtOpenGL.QGLBuffer.StaticDraw);
            vertex_buffer.allocate(len(buffer_object._vertex_buffer));
            vertex_buffer.write(0, buffer_object._vertex_buffer, len(buffer_object._vertex_buffer));
            self._vertex_buffers.append(vertex_buffer)

            index_buffer = QtOpenGL.QGLBuffer(QtOpenGL.QGLBuffer.IndexBuffer)
            index_buffer.create();
            index_buffer.bind();
            index_buffer.setUsagePattern(QtOpenGL.QGLBuffer.StaticDraw);
            index_buffer.allocate(len(buffer_object._index_buffer));
            index_buffer.write(0, buffer_object._index_buffer, len(buffer_object._index_buffer));
            self._index_buffers.append(index_buffer)

    def resizeGL(self, w, h):
        logging.warning("resizeGL")

    def paintGL(self):
        for mesh in self._model._meshes:

            self._buffer_object_id = None

            self._vertex_buffer_offset = None
            self._vertex_count = None
            self._vertex_size = None

            self._index_buffer_offset = None
            self._index_count = None

            self._read(file_handle)

        glBindBuffer(GL_ARRAY_BUFFER, staticBuffer);
        glEnableClientState(GL_VERTEX_ARRAY);
        glVertexPointer(2, GL_FLOAT, sizeof(vertexStatic), (void*)offsetof(vertexStatic,position));
        glBindBuffer(GL_ARRAY_BUFFER, dynamicBuffer);
        glEnableClientState(GL_COLOR_ARRAY);
        glColorPointer(4, GL_UNSIGNED_BYTE, sizeof(vertexDynamic), (void*)offsetof(vertexDynamic,color));
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBuffer);
        glDrawElements(GL_TRIANGLE_STRIP, sizeof(indices)/sizeof(GLubyte), GL_UNSIGNED_BYTE, (void*)0);
     #     void initializeGL()
     # {
     #     // Set up the rendering context, define display lists etc.:
     #     ...
     #     glClearColor(0.0, 0.0, 0.0, 0.0);
     #     glEnable(GL_DEPTH_TEST);
     #     ...
     # }

     # void resizeGL(int w, int h)
     # {
     #     // setup viewport, projection etc.:
     #     glViewport(0, 0, (GLint)w, (GLint)h);
     #     ...
     #     glFrustum(...);
     #     ...
     # }

     # void paintGL()
     # {
     #     // draw the scene:
     #     ...
     #     glRotatef(...);
     #     glMaterialfv(...);
     #     glBegin(GL_QUADS);
     #     glVertex3f(...);
     #     glVertex3f(...);
     #     ...
     #     glEnd();
     #     ...
     # }

def main():
    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmgui')

    dat_manager = DatManager(config.get('game', 'path'))

    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QWidget()
    main_window.setWindowTitle('Model Viewer')

    opengl_widget = OpenGLWidget(dat_manager)

    layout = QtGui.QHBoxLayout()
    layout.addWidget(opengl_widget)

    main_window.setLayout(layout)
    main_window.resize(640, 480)
    main_window.show()

    model = Model('chara/monster/m0104/obj/body/b0001/model/m0104b0001.mdl', dat_manager.get_file('chara/monster/m0104/obj/body/b0001/model/m0104b0001.mdl'))
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()