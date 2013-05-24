# -*- coding: utf-8 -*-

import sys
import logging
from configparser import SafeConfigParser

from PyQt4 import QtGui, QtOpenGL

from xivdm.dat.Manager import Manager as DatManager
from xivdm.cache.Manager import Manager as CacheManager
from xivdm.logging_utils import set_logging

def process_item(parent, obj):
    if type(obj) == dict:
        for key, value in obj.items():
            new_item = QtGui.QTreeWidgetItem(parent, [key])
            parent.addChild(new_item)
            process_item(new_item, value)

def main():
    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmgui')

    dat_manager = DatManager(config.get('game', 'path'))
    cache_manager = CacheManager(dat_manager)

    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QWidget()
    main_window.setWindowTitle('Model Viewer')

    tree_widget = QtGui.QTreeWidget()
    tree_widget.setHeaderLabels(['dat'])

    for category_name in sorted(cache_manager.get_categories()):
        category_widget_item = QtGui.QTreeWidgetItem(tree_widget, [category_name])
        tree_widget.addTopLevelItem(category_widget_item)
        category = cache_manager.get_category(category_name)
        process_item(category_widget_item, category)

    opengl_widget = QtOpenGL.QGLWidget()

    splitter = QtGui.QSplitter()
    splitter.addWidget(tree_widget)
    splitter.addWidget(opengl_widget) 

    layout = QtGui.QHBoxLayout()
    layout.addWidget(splitter)

    main_window.setLayout(layout)
    main_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()