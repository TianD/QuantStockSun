# coding:utf-8
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from core.ActionThread import ActionThread
from core.AutoAction import ClickAction, PressAction, OCRAction
from ui.ActionModel import ActionModel
from ui.ActionTableView import ActionTableView


class AutoActionManager(QtWidgets.QWidget):
    dataChanged = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(AutoActionManager, self).__init__(parent)

        self.setupUi(self)
        self.initDataBefore()
        self.bindFuncs()
        self.initDataAfter()

    def setupUi(self, parent):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        action_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(action_layout)
        self.action_label = QtWidgets.QLabel('创建Action:')
        action_layout.addWidget(self.action_label)
        self.action_combo_box = QtWidgets.QComboBox()
        action_layout.addWidget(self.action_combo_box)
        self.action_btn = QtWidgets.QPushButton('创建')
        action_layout.addWidget(self.action_btn)

        self.action_view = ActionTableView()
        main_layout.addWidget(self.action_view)
        self.action_model = ActionModel()
        self.action_view.setModel(self.action_model)

        caller_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(caller_layout)
        self.caller_timer_label = QtWidgets.QLabel('调用间隔(分钟)')
        caller_layout.addWidget(self.caller_timer_label)
        self.caller_timer_line_edit = QtWidgets.QSpinBox()
        caller_layout.addWidget(self.caller_timer_line_edit)
        self.caller_btn = QtWidgets.QPushButton('开始')
        caller_layout.addWidget(self.caller_btn)
        self.caller_esc_label = QtWidgets.QLabel('按ESC取消')
        main_layout.addWidget(self.caller_esc_label)

    def initDataBefore(self):
        self.action_combo_box.addItem(ClickAction.name, ClickAction)
        self.action_combo_box.addItem(PressAction.name, PressAction)
        self.action_combo_box.addItem(OCRAction.name, OCRAction)
        self.action_thread = ActionThread()

    def bindFuncs(self):
        self.action_btn.clicked.connect(self.create_action)
        self.caller_btn.clicked.connect(self.run_action)
        self.action_thread.output.connect(self.show_result)

    def initDataAfter(self):
        pass

    def create_action(self):
        current_index = self.action_combo_box.currentIndex()
        item = self.action_combo_box.itemData(current_index)
        self.action_model.insertRow(item())

    def run_action(self):
        self.caller_btn.setDisabled(True)
        caller_timer = int(self.caller_timer_line_edit.text())
        action_list = self.action_model.source_data
        self.action_thread.set_action_list(action_list)
        self.action_thread.set_timer(caller_timer)
        self.action_thread.start()

    def show_result(self, data):
        self.activateWindow()
        self.dataChanged.emit(data)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.action_thread.isRunning():
                self.action_thread.terminate()
                self.action_thread.wait(1)
            self.caller_btn.setEnabled(True)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    win = AutoActionManager()
    win.show()
    app.exec_()
