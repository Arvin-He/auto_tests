
import cProfile
import datetime
import os
import pstats
import subprocess
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import gevent
import gevent.monkey
import pyautogui
import py
import pytest
import _pytest

import basic
from basic import R
from common.coordinate.coordinatedialog import CoordinateDialog

# 相关路径初始化
__dir__ = os.path.dirname(os.path.abspath(__file__))
_test_helpers_dir = __dir__
_root_dir = os.path.dirname(_test_helpers_dir)
_tests_dir = os.path.join(_root_dir, "tests")


# 配置
_profile = os.environ.get("PUNGGOL_TESTS_PROFILE") == "1"


# gevent monkey patch
gevent.monkey.patch_time()  # 将 time.sleep 替换为 gevent.sleep


# pyautogui 配置
pyautogui.MINIMUM_DURATION = 0.1
pyautogui.MINIMUM_SLEEP = 0.02
pyautogui.PAUSE = 0.2
pyautogui.FAILSAFE = False
pyautogui.FailSafeException = _pytest.runner.Exit


# iniconfig 补丁, 解决 pytest.ini 不能是 UTF-8 编码的问题
if sys.platform == "win32" and py.iniconfig.IniConfig.__name__ != "_IniConfig_fix":
    class _IniConfig_fix(py.iniconfig.IniConfig):

        def __init__(self, path, data=None):
            if data is None:
                with open(str(path), encoding="utf-8") as f:
                    data = f.read()
            super(_IniConfig_fix, self).__init__(path, data)
    py.iniconfig.IniConfig = _IniConfig_fix


# 测试运行控制
_test_greenlet = None


def _test_main(args):
    os.chdir(_tests_dir)
    try:
        if sys.platform == "win32":
            subprocess.check_call("cls", shell=True)

        if _profile:
            profile = cProfile.Profile()
            profile.enable()

        basic.mainWindow.showNormal()
        basic.mainWindow.raise_()
        basic.mainWindow.activateWindow()
        QtWidgets.qApp.processEvents()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        test_report_file = os.path.join(_root_dir, "reports", "{}_tests.html".format(timestamp))
        pytest.main(["--capture=no", "--html", test_report_file, "--self-contained-html"] + args)
    finally:
        if _profile:
            profile.disable()
            pstats.Stats(profile).sort_stats("time").print_stats(20)

        # 避免警告
        if "pytest_timeout" in sys.modules:
            del sys.modules["pytest_timeout"]

        # 卸载测试模块, 从而下次执行测试时能重新加载修改后的文件
        test_modules = []
        for name, module in sys.modules.items():
            if hasattr(module, "__file__") and module.__file__.startswith(_root_dir):
                test_modules.append(name)
        for name in test_modules:
            del sys.modules[name]

        global _test_greenlet
        _test_greenlet = None


@basic.api
def run_tests(args):
    global _test_greenlet
    _test_greenlet = gevent.spawn(_test_main, args)


@basic.api
def stop_tests():
    _test_greenlet.kill(_pytest.runner.Exit("用户中止测试"))


@basic.api
def tests_running():
    return _test_greenlet is not None


# 常用功能封装
sleep = gevent.sleep


def msleep(ms):
    sleep(ms * 0.001)


def moveTo(x=None, y=None, pt=None, widget=None):
    if widget is not None:
        pt = widget.mapToGlobal(widget.rect().center())
    if pt is not None:
        x, y = pt.x(), pt.y()
    pyautogui.moveTo(x, y, duration=0.2)


mouseDown = pyautogui.mouseDown
mouseUp = pyautogui.mouseUp


def click(x=None, y=None, pt=None, widget=None):
    moveTo(x, y, pt, widget)
    mouseDown()
    mouseUp()


typewrite = pyautogui.typewrite
press = pyautogui.press
keyDown = pyautogui.keyDown
keyUp = pyautogui.keyUp
hotkey = pyautogui.hotkey
rightClick = pyautogui.rightClick


def screenshot():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = os.path.join(_root_dir, "reports", "{}_screenshot.png".format(timestamp))
    pyautogui.screenshot(screenshot_file, basic.mainWindow.geometry().getRect())


def assertActiveWindow(obj):
    win = QtWidgets.QApplication.activeWindow()
    assert win is not None
    assert win is obj or isinstance(win, obj)
    return win


def close(win):
    moveTo(pt=win.mapToGlobal(win.rect().topRight() - QtCore.QPoint(10, 10)))
    pyautogui.click()  # 关闭按钮不能通过 mouseDown, mouseUp 来点击, mouseDown 会导致消息循环卡住


_mainWindowContent = basic.mainWindow.findChild(
    QtWidgets.QWidget, "MainPage", QtCore.Qt.FindDirectChildrenOnly)


def findButtons(win, text):
    # 缩小查找范围
    if win is basic.mainWindow:
        win = _mainWindowContent
    buttons = win.findChildren(QtWidgets.QAbstractButton)
    return [button for button in buttons if button.text() == text]


def clickButton(win, text):
    buttons = findButtons(win, text)
    assert buttons, "未找到按钮"
    click(widget=buttons[0])


def assertActiveMenu():
    popup = QtWidgets.QApplication.activePopupWidget()
    assert isinstance(popup, QtWidgets.QMenu)
    return popup


def clickMenu(text=None, action=None):
    menu = assertActiveMenu()
    if action is None:
        for item in menu.actions():
            if item.text() == text:
                action = item
                break
        assert action, "未找到菜单"
    click(pt=menu.mapToGlobal(menu.actionGeometry(action).center()))


def clickTable(widget, row=None, column=None, item=None):
    if item is None:
        item = widget.item(row, column)
    click(pt=widget.mapToGlobal(widget.visualItemRect(item).center()))


def lineEditTypewrite(text, lineEdit):
    click(widget=lineEdit)
    msleep(500)
    hotkey('ctrl', 'a')
    msleep(500)
    typewrite(text)
    msleep(500)
    press("enter")


def loadProgram(filename):
    basic.unloadProgram()
    msleep(1500)
    basic.loadProgram(filename)


def startSetup():
    # 切换到开发商权限
    basic._private.auth._Set_Auth_Level(0)
    # 置为已回零状态
    for i in range(basic.axisCount()):
        R[641 + i] = 1
    # 配置工件偏移、材料厚度、外部偏移
    assertActiveWindow(basic.mainWindow)
    clickButton(basic.mainWindow, "坐标设定")
    msleep(1000)
    win = assertActiveWindow(CoordinateDialog)
    offset_x = win.ui.offset_x
    offset_y = win.ui.offset_y
    thickness = win.ui.groupBox_4.findChildren(QtWidgets.QLineEdit)
    external_offset = win.ui.groupBox_3.findChildren(QtWidgets.QLineEdit)
    msleep(1000)
    lineEditTypewrite("160", offset_x)
    lineEditTypewrite("-160", offset_y)
    for thick in thickness:
        lineEditTypewrite("-50", thick)
        msleep(1000)
    for external in external_offset:
        lineEditTypewrite("0", external)
        msleep(1000)
    close(win)
    msleep(1000)