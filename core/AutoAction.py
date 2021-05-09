# coding:utf-8
import tempfile
from datetime import datetime

import pandas as pd
import pyautogui
from PySide2 import QtGui, QtCore

from core.ocr import get_file_content, get_aliyun_ocr_result
from libs.pyqt_screenshot import constant
from libs.pyqt_screenshot.screenshot import Screenshot


class AutoAction(object):

    name = 'AutoAction'

    def __init__(self, cmd, args):
        self.__cmd = cmd
        self.__args = args

    @property
    def cmd(self):
        return self.__cmd

    @property
    def args(self):
        return self.__args

    def set_args(self, value):
        self.__args = value

    def run(self):
        result = self.cmd(self.args)


class ClickAction(AutoAction):

    name = '点击'

    def __init__(self):
        super(ClickAction, self).__init__(pyautogui.click, '')
        self.__cmd = pyautogui.click
        self.__args = ''

    @property
    def cmd(self):
        return self.__cmd

    @property
    def args(self):
        return self.__args

    @property
    def showed_args(self):
        return self.args

    def set_args(self, value):
        self.__args = value

    def run(self):
        print(self.args)
        x, y = self.args.split(',')
        args = {'x': int(x), 'y': int(y)}
        result = self.cmd(**args)


class PressAction(AutoAction):

    name = '输入'

    def __init__(self):
        super(PressAction, self).__init__(pyautogui.press, '')
        self.__cmd = pyautogui.press
        self.__args = ''

    @property
    def cmd(self):
        return self.__cmd

    @property
    def args(self):
        return self.__args

    @property
    def showed_args(self):
        return self.args

    def set_args(self, value):
        self.__args = value

    def run(self):
        content = list(self.args)
        result = self.cmd(content)
        return {'content': result}


class OCRAction(AutoAction):

    name = '表格识别'

    def __init__(self):
        pos = Screenshot.take_screenshot_pos(constant.CLIPBOARD)
        self.__args = pos
        print(self.__args)

    @property
    def args(self):
        return self.__args

    @property
    def showed_args(self):
        return '%s,%s,%s,%s' %(self.args.top(), self.args.left(),
                               self.args.right(), self.args.bottom())

    def set_args(self, value):
        self.__args = value

    def run(self):
        screen = QtGui.QGuiApplication.screens()[0]
        screen_pixel = screen.grabWindow(0)
        img = screen_pixel.copy(self.args)
        img_path = '%s/%s.jpg' % (tempfile.gettempdir(), datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        img.save(img_path)
        base64_data = get_file_content(img_path)
        data = get_aliyun_ocr_result(base64_data)
        print(data)
        # data = pd.read_excel(xlsx_data)

        return {'img': data}
