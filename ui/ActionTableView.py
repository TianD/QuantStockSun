# coding: utf-8

from PySide2 import QtWidgets, QtCore


class ActionTableView(QtWidgets.QTableView):

    def __init__(self, parent=None):
        super(ActionTableView, self).__init__(parent)

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Delete:
            model = self.model()
            selected = self.selectedIndexes()
            rows = list(set([index.row() for index in selected]))
            for row in rows[::-1]:
                model.removeRow(row)
