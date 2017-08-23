#!/user/bin/env python3
# @Author: Grace
import unittest
import testhelpers as th
import basic
from basic import F, R


class SingleExec(unittest.TestCase):

    def setUp(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)

    def tearDown(self):
        pass

    def test_SingleExec(self):
        # 加载测试NC程序
        basic.loadProgram("E:/NC/自动测试程序/single_test.NC")
        th.msleep(500)
        th.clickButton(basic.mainWindow, "单段执行")
        th.msleep(500)
        th.clickButton(basic.mainWindow, "F11 开始")
        th.msleep(1000)
        # 判断是否处于单段保持状态
        assert F[2] == 1
        # 判断走完一行之后的坐标
        assert R[101] == 100000000 and R[102] == -100000000
        for i in range(basic.spindleCount()):
            assert R[103 + i] == -20000000

        th.clickButton(basic.mainWindow, "F11 开始")
        th.msleep(1000)
        # 判断是否处于单段保持状态
        assert F[2] == 1
        # 判断走完一行之后的坐标
        assert R[101] == 130000000 and R[102] == -100000000
        for i in range(basic.spindleCount()):
            assert R[103 + i] == -20000000

        th.clickButton(basic.mainWindow, "F11 开始")
        th.msleep(1000)
        # 判断是否处于单段保持状态
        assert F[2] == 1
        # 判断走完一行之后的坐标
        assert R[101] == 130000000 and R[102] == -130000000
        for i in range(basic.spindleCount()):
            assert R[103 + i] == -20000000

        th.clickButton(basic.mainWindow, "F11 开始")
        th.msleep(1000)
        # 判断是否处于单段保持状态
        assert F[2] == 1
        # 判断走完一行之后的坐标
        assert R[101] == 100000000 and R[102] == -130000000
        for i in range(basic.spindleCount()):
            assert R[103 + i] == -20000000

        th.clickButton(basic.mainWindow, "F11 开始")
        th.msleep(1000)
        # 判断是否处于单段保持状态
        assert F[2] == 1
        # 判断走完一行之后的坐标
        assert R[101] == 100000000 and R[102] == -100000000
        for i in range(basic.spindleCount()):
            assert R[103 + i] == -20000000

        th.clickButton(basic.mainWindow, "F11 开始")
        th.msleep(1000)
        # 判断加工结束后，是否回到准备好状态
        assert F[3] == 1
        # 判断加工结束后，回到固定点
        assert R[101] == R[102] == 0
        for i in range(basic.spindleCount()):
            assert R[103 + i] == 0
