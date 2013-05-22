# -*- coding: utf-8 -*-

import sys
import logging
from configparser import SafeConfigParser

from PyQt4 import QtGui, QtOpenGL

from xivdm.dat.Manager import Manager as DatManager
from xivdm.logging_utils import set_logging

def process_item(parent, dir_map):
    for name in sorted(list(dir_map.keys()))[::-1]:
        new_item = QtGui.QTreeWidgetItem(parent, [name])
        parent.addChild(new_item)
        if dir_map[name]:
            process_item(new_item, dir_map[name])

def main():
    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmgui')

    dat_manager = DatManager(config.get('game', 'path'))

    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QWidget()
    main_window.setWindowTitle('Model Viewer')

    tree_widget = QtGui.QTreeWidget()
    tree_widget.setHeaderLabels(['dat'])

    dirs = {}
    for category_name in dat_manager.get_categories():
        dirs[category_name] = {}
        category = dat_manager.get_category(category_name)
        for dir_hash in category.get_hash_table().keys():
            dir_name = dat_manager.get_dir_name(category_name, dir_hash)
            current_dir = dirs[category_name]
            for name in dir_name.split('/'):
                if name == category_name:
                    continue
                if not name in current_dir:
                    current_dir[name] = {}
                current_dir = current_dir[name]

            current_dir.update({
                dat_manager.get_file_name(category_name, dir_hash, file_hash): None for file_hash in category.get_dir_hash_table(dir_hash).keys()
                })

    for category_name in sorted(list(dirs.keys()))[::-1]:
        category_widget_item = QtGui.QTreeWidgetItem(tree_widget, [category_name])
        tree_widget.addTopLevelItem(category_widget_item)

        process_item(category_widget_item, dirs[category_name])

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