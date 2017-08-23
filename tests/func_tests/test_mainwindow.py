# !/user/bin/python
# -*- coding:utf-8 -*-
# @Author:Grace
import unittest

import testhelpers as th
import basic
from common.widgets.pushbutton import PyPushButton
from basic import R


class MainUI(unittest.TestCase):
    def test_MainUI(self):
        for i in range(basic.axisCount()):
            R[641 + i] = 1
        from plugins.mainui.mainwindow import _mainWindowContent
        _mainWindowContent.ui.F1.animateClick()
        th.msleep(3000)
        _mainWindowContent.ui.F2.animateClick()
        th.msleep(3000)

        # print(_mainWindowContent.ui.frame_2.findChildren(PyPushButton))
        ls = _mainWindowContent.ui.frame_2.findChildren(PyPushButton)
        autotool = _mainWindowContent.ui.frame_2.findChild(PyPushButton, 'PushButton_7')
        for i in range(len(ls)):
            if ls[i] == autotool:
                continue
                th.msleep(2000)
            else:
                th.msleep(1000)
                ls[i].animateClick()
                th.msleep(500)
                ls[i].animateClick()
