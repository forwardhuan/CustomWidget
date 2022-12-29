#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# ======================================================
# @File:  : multi_copy_table
# @Author : forward_huan
# @Date   : 2022/12/29 22:12
# @Desc   : 支持复制多个单元格内容的QTableWidget
# ======================================================
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QApplication, QTableWidgetItem


class TableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.is_multi_copy = False

    @staticmethod
    def is_ctrl_c_pressed(event: QtGui.QKeyEvent):
        """
        Ctrl + C是否同时按下

        :param event:
        :return:
        """
        return event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier)

    def set_support_multi_copy(self, is_support: bool):
        """
        设置是否同时支持复制多个单元格

        :param is_support:
        :return:
        """
        self.is_multi_copy = is_support

    def copu_multi(self):
        """
        复制多个选中单元格的内容到剪切板

        :return:
        """
        items = self.selectedItems()
        if not items:
            return
        select_data = [[item.row(), item.column(), item.text()] for item in items]
        row_data = [item[0] for item in select_data]
        col_data = [item[1] for item in select_data]
        row_min, row_max = min(row_data), max(row_data)
        col_min, col_max = min(col_data), max(col_data)
        data = [[""] * (col_max - col_min + 1) for _ in range(row_max - row_min + 1)]
        for item in select_data:
            row, col, text = item
            data[row - row_min][col - col_min] = text
        QApplication.clipboard().setText("\n".join(["\t".join(item) for item in data]))

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if self.is_multi_copy and self.is_ctrl_c_pressed(event):
            self.copu_multi()
            return
        super(TableWidget, self).keyPressEvent(event)


def run():
    app = QApplication(sys.argv)
    table_widget = TableWidget()
    table_widget.set_support_multi_copy(True)
    table_widget.resize(800, 600)
    table_widget.setRowCount(6)
    table_widget.setColumnCount(4)

    table_widget.setHorizontalHeaderLabels([f"第{i}列" for i in range(table_widget.columnCount())])
    table_widget.setVerticalHeaderLabels([f"第{i}行" for i in range(table_widget.rowCount())])
    for row in range(table_widget.rowCount()):
        for col in range(table_widget.columnCount()):
            table_widget.setItem(row, col, QTableWidgetItem(f"test_{row}_{col}"))
    table_widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
