#!/user/bin/env python3
# @Author: Grace

import unittest
import basic
from basic import F, P, R
import testhelpers as th
import random
from PyQt5 import QtWidgets
import pytest


class Home(unittest.TestCase):

    def setUp(self):
        th.msleep(1000)
        # 获取寻原点方向初始值
        self.origin_dir = []
        for i in range(basic.axisCount()):
            self.origin_dir.append(P[1701 + i])
        # 打开Home对话框
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "Home")
        th.msleep(1000)
        # 判断当前窗口是否为Home对话框
        self.homewindow = th.assertActiveWindow(basic.HomeDialog)

    def tearDown(self):
        th.close(self.homewindow)
        # 恢复XYZ寻原点方向初始值
        for i in range(basic.axisCount()):
            P[1701 + i] = self.origin_dir[i]

    # 定义一个模拟按键函数
    def push_key(self):
        th.msleep(500)
        F[588] = True
        th.msleep(500)
        F[588] = False
        th.msleep(500)
        F[590] = True
        th.msleep(500)
        F[590] = False
        th.msleep(500)
        F[590] = True
        th.msleep(500)
        F[590] = False
        th.msleep(500)

    # 手动Home
    def test_Manul_Home(self):
        # 获取键盘
        F[400] = True
        # 将X寻原点方向设为1，YZ寻原点方向设为0
        P[1701] = 1
        for i in range(basic.axisCount() - 1):
            P[1702 + i] = 0

        if P[4138] == 0:
            # 点击所有轴Home按钮
            th.clickButton(self.homewindow, "所有轴Home")
            th.msleep(1000)
            # 判断是否是Z轴先Home
            assert R[41] == 1 and R[42] == 1
            for i in range(basic.spindleCount()):
                R[43 + i] == 0
            self.push_key()
            # 判断是否ZHome完成后，xy开始Home
            assert R[41] == 0 and R[42] == 0
            for i in range(basic.spindleCount()):
                R[43 + i] == 1
            self.push_key()
            # 判断xyZ是否都Home成功
            assert R[41] == 1 and R[42] == 1
            for i in range(basic.spindleCount()):
                R[43 + i] == 1

            # 单轴Home
            # X轴Home
            th.clickButton(self.homewindow, "X 轴Home")
            th.msleep(1000)
            # 判断X轴Home方向
            th.msleep(200)
            v1 = R[101]
            th.msleep(500)
            v2 = R[101]
            assert v1 > v2
            th.msleep(500)
            F[588] = True
            th.msleep(500)
            F[588] = False
            # 判断粗定位完成后,X轴Home方向
            th.msleep(200)
            v3 = R[101]
            th.msleep(200)
            v4 = R[101]
            assert v3 < v4
            th.msleep(500)
            F[590] = True
            th.msleep(500)
            F[590] = False
            th.msleep(500)
            F[590] = True
            th.msleep(500)
            F[590] = False
            th.msleep(500)

            # Y轴Home
            th.clickButton(self.homewindow, "Y 轴Home")
            th.msleep(1000)
            # 判断Y轴Home方向
            th.msleep(200)
            v1 = R[102]
            th.msleep(500)
            v2 = R[102]
            assert v1 < v2
            th.msleep(500)
            F[588] = True
            th.msleep(500)
            F[588] = False
            # 判断粗定位完成后,Y轴Home方向
            th.msleep(200)
            v3 = R[102]
            th.msleep(200)
            v4 = R[102]
            assert v3 > v4
            th.msleep(500)
            F[590] = True
            th.msleep(500)
            F[590] = False
            th.msleep(500)
            F[590] = True
            th.msleep(500)
            F[590] = False
            th.msleep(500)

            # Z轴Home
            i = random.randint(1, basic.spindleCount())
            th.clickButton(self.homewindow, "Z{} 轴Home".format(i))
            th.msleep(1000)
            # 判断Z轴Home方向
            th.msleep(200)
            v1 = R[102 + i]
            th.msleep(500)
            v2 = R[102 + i]
            assert v1 < v2
            th.msleep(500)
            F[588] = True
            th.msleep(500)
            F[588] = False
            # 判断粗定位完成后,Z轴Home方向
            th.msleep(200)
            v3 = R[102 + i]
            th.msleep(200)
            v4 = R[102 + i]
            assert v3 > v4
            th.msleep(500)
            F[590] = True
            th.msleep(500)
            F[590] = False
            th.msleep(500)
            F[590] = True
            th.msleep(500)
            F[590] = False
            th.msleep(500)

            # 选择任意一个Z轴Home
            th.msleep(1000)
            th.clickButton(self.homewindow, "Z{} 轴Home".format(random.randint(1, basic.spindleCount())))
            th.msleep(500)
            # 停止Home
            th.clickButton(basic.mainWindow, "F12 停止")

            # Z轴未Home的情况下,XHome
            th.msleep(500)
            th.clickButton(self.homewindow, "X 轴Home")
            th.msleep(500)
            msg = th.assertActiveWindow(QtWidgets.QMessageBox)
            th.clickButton(msg, "是(&Y)")
            self.push_key()
            # Z轴未Home的情况下,点击YHome并取消YHome
            th.msleep(500)
            th.clickButton(self.homewindow, "Y 轴Home")
            th.msleep(500)
            msg = th.assertActiveWindow(QtWidgets.QMessageBox)
            th.clickButton(msg, "否(&N)")

            # 勾选重启软件自动Home
            P[4138] = 1

    # 自动Home
    @pytest.mark.group("restart")
    def test_Auto_Home(self):
        # 检查是否开机后软件自动Home
        for i in range(basic.spindleCount()):
            R[43 + i] == 1
        # 获取键盘
        F[400] = True
        # 模拟Home信号按键
        self.push_key()

        # 检查是否是Z先Home完成，XY再Home
        assert R[41] == 0 and R[42] == 0
        for i in range(basic.spindleCount()):
            R[43 + i] == 1
        self.push_key()

        # 检查是否都Home完成
        assert R[41] == 1 and R[42] == 1
        for i in range(basic.spindleCount()):
            R[43 + i] == 1

        # 勾消重启软件后自动Home
        th.msleep(500)
        P[4138] = 0
