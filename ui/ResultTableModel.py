# coding: utf-8

from PySide2 import QtCore


class ResultTableModel(QtCore.QAbstractTableModel):

    def __init__(self, header_list=None, source_data=None, parent=None):
        super(ResultTableModel, self).__init__(parent)

        self.__header_list = header_list or []
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
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return
        row = index.row()
        column = index.column()
        key = self.header_list[column]
        if role == QtCore.Qt.DisplayRole:
            return self.source_data[row][key]
        else:
            return

    def update_source_data(self, value):
        self.beginResetModel()
        self.source_data = value
        self.endResetModel()

    def insertRow(self, value, parent=QtCore.QModelIndex()):
        first = len(self.source_data)
        self.beginInsertRows(parent, first, first)
        self.source_data.append(value)
        self.endInsertRows()
