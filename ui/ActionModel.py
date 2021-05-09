# coding: utf-8

from PySide2 import QtCore


class ActionModel(QtCore.QAbstractTableModel):

    def __init__(self, source_data=None, parent=None):
        super(ActionModel, self).__init__(parent)

        self.__header_list = ['Action', 'Args']
        self.__source_data = source_data or []

    @property
    def header_list(self):
        return self.__header_list

    @header_list.setter
    def header_list(self, value):
        if isinstance(value, list):
            self.__header_list = value
        else:
            raise TypeError('expected a list object, but got a %s object.' % type(value).__name__)

    @property
    def source_data(self):
        return self.__source_data

    @source_data.setter
    def source_data(self, value):
        if isinstance(value, list):
            self.__source_data = value
        else:
            raise TypeError('expected a list object, but got a %s object.' % type(value).__name__)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_list[section]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.source_data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.header_list)

    def flags(self, index):
        if index.isValid():
            column = index.column()
            if column == 1:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if column == 0:
                return self.source_data[row].name
            elif column == 1:
                return self.source_data[row].showed_args
            else:
                return
        else:
            return

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False
        row = index.row()
        column = index.column()
        if column == 0:
            return False
        self.source_data[row].set_args(value)
        return True

    def update_source_data(self, value):
        self.beginResetModel()
        self.source_data = value
        self.endResetModel()

    def insertRow(self, value, parent=QtCore.QModelIndex()):
        first = len(self.source_data)-1
        last = first
        self.beginInsertRows(parent, first, last)
        self.source_data.append(value)
        self.endInsertRows()

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        self.source_data.pop(row)
        self.endRemoveRows()
