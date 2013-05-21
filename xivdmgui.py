# -*- coding: utf-8 -*-

import sys
from configparser import SafeConfigParser

from PyQt4 import QtGui, QtOpenGL

from xivdm.dat.Manager import Manager as DatManager


def main():
    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    dat_manager = DatManager(config.get('game', 'path'))

    app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QWidget()
    main_window.setWindowTitle('Model Viewer')

    tree_widget = QtGui.QTreeWidget()
    tree_widget.setHeaderLabels(["dat_tree"])
    for category_name in dat_manager.get_categories():
        category = dat_manager.get_category(category_name)
        category_widget_item = QtGui.QTreeWidgetItem(tree_widget, [category_name])
        tree_widget.addTopLevelItem(category_widget_item)
        for dir_hash in category.get_hash_table().keys():
            dir_widget_item = QtGui.QTreeWidgetItem(category_widget_item, ['%0.8X' % dir_hash])
            category_widget_item.addChild(dir_widget_item)
            dir_widget_item.addChildren([QtGui.QTreeWidgetItem(dir_widget_item, ['%0.8X' % file_hash]) for file_hash in category.get_dir_hash_table(dir_hash).keys()])

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