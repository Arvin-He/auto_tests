# !/user/bin/env python
# @Author:Grace
import unittest
import basic
from basic import F, R, P, Y
from basic.unit import BLU
import testhelpers as th
import random
from PyQt5 import QtWidgets


@unittest.skipIf(not th.findButtons(basic.mainWindow, "AutoToolSet"), "没有AutoToolSet功能")
class AutoToolSet(unittest.TestCase):
    def setUp(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)

    def test_AutoToolSet(self):
        # 获取键盘
        F[400] = True

        # 单头机
        if basic.spindleCount() == 1:

            th.clickButton(basic.mainWindow, "AutoToolSet")
            th.msleep(1000)
            msg = th.assertActiveWindow(QtWidgets.QMessageBox)
            th.msleep(500)
            th.clickButton(msg, "确定")
            th.msleep(500)
            # 点击完AutoToolSet，判断输出端口对刀吹气是否为ture
            assert Y[7]
            th.msleep(1500)
            # 判断XY是否到达对刀起始高度
            assert R[101] == round(P[1621] / BLU, 1) and R[102] == round(P[1622] / BLU, 1)
            # 判断XYZ是否到达对刀起始高度后，关闭吹气
            self.assertFalse(Y[7])
            th.msleep(1000)
            F[590] = True
            # 判断对刀时，第一次触碰对刀信号后,Z轴抬高
            th.msleep(200)
            v1 = R[103]
            th.msleep(200)
            v2 = R[103]
            assert v1 < v2
            th.msleep(1000)
            F[590] = False
            th.msleep(500)
            F[590] = True
            th.msleep(500)
            F[590] = False
            th.msleep(2000)

            # 判断 取消AutoToolSet后 XYZ轴不动
            v1_x = R[101]
            v1_y = R[102]
            v1_z = R[103]
            th.clickButton(basic.mainWindow, "AutoToolSet")
            th.msleep(1000)
            msg = th.assertActiveWindow(QtWidgets.QMessageBox)
            th.msleep(1000)
            th.clickButton(msg, "取消")
            v2_x = R[101]
            v2_y = R[102]
            v2_z = R[103]
            assert v1_x == v2_x and v1_y == v2_y and v1_z == v2_z

        else:
            # 多头机对刀
            th.clickButton(basic.mainWindow, "AutoToolSet")
            th.msleep(1000)
            msg = th.assertActiveWindow(basic.AutomaticToolDialog)
            th.msleep(1000)
            th.clickButton(msg, "对刀开始")
            th.msleep(2000)
            # 判断XYZ是否到达对刀起始高度
            assert R[101] == round(P[1621] / BLU, 1) and R[102] == round(P[1622] / BLU, 1)
            th.msleep(1000)

            F[590] = True
            # 判断对刀时，第一次触碰对刀信号后,Z轴抬高
            th.msleep(200)
            v1 = R[103]
            th.msleep(200)
            v2 = R[103]
            assert v1 < v2
            th.msleep(1000)
            F[590] = False
            th.msleep(500)
            F[590] = True
            th.msleep(1000)
            F[590] = False
            th.msleep(3000)

            # 不勾选所有Z轴
            th.clickButton(basic.mainWindow, "AutoToolSet")
            th.msleep(1000)
            R[1007, random.randint(0, basic.spindleCount() - 1)] = 0
            th.msleep(1000)
            msg = th.assertActiveWindow(basic.AutomaticToolDialog)
            th.clickButton(msg, "对刀开始")
            th.msleep(2000)
            F[590] = True
            th.msleep(1000)
            F[590] = False
            th.msleep(500)
            F[590] = True
            th.msleep(1000)
            F[590] = False
            th.msleep(3000)
