# coding:utf-8
from datetime import datetime

from PySide2 import QtCore


class ActionThread(QtCore.QThread):

    output = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(ActionThread, self).__init__(parent)
        self.__action_list = []
        self.__timer = 0

    @property
    def action_list(self):
        return self.__action_list

    @property
    def timer(self):
        return self.__timer

    def set_timer(self, timer):
        self.__timer = timer

    def set_action_list(self, action_list):
        self.__action_list = action_list

    def run(self):
        while True:
            self.sleep(self.timer*10)
            data = {'current_time': datetime.now()}
            for action in self.action_list:
                result = action.run()
                for key, value in result.items():
                    if isinstance(value, dict):
                        data.setdefault(key, {}).update(value)
                    elif isinstance(value, list):
                        data.setdefault(key, []).append(value)
                    else:
                        data.update({key: value})
            self.output.emit(data)

