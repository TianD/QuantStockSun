# coding:utf-8
from pprint import pprint

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from ui.AutoActionManager import AutoActionManager
from ui.ResultTableModel import ResultTableModel


class MainWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.setupUi(self)
        self.initDataBefore()
        self.bindFuncs()
        self.initDataAfter()

    def setupUi(self, parent):
        self.setWindowTitle('Quant Stock Sun')
        self.setWindowFlags(QtCore.Qt.Window)
        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        self.action_manager = AutoActionManager()
        main_layout.addWidget(self.action_manager)
        self.result_table = QtWidgets.QTableView()
        main_layout.addWidget(self.result_table)

    def initDataBefore(self):
        self.result_model = ResultTableModel()
        self.result_table.setModel(self.result_model)

    def bindFuncs(self):
        self.action_manager.dataChanged.connect(self.add_row)

    def initDataAfter(self):
        pass

    def add_row(self, data):
        new_data = data.get('img')
        pprint(new_data)
        self.result_model.update_header_list(list(new_data.keys()))
        self.result_model.insertRow(new_data)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    win = MainWidget()
    win.show()
    app.exec_()
