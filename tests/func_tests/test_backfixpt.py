#!/user/bin/env python3
# @Author: Grace

import unittest
import basic
from basic import R, P
import testhelpers as th
from basic.unit import mm, minute, BLU


class 回固定点(unittest.TestCase):

    def setUp(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)

        # 获取快速定位速度初始值
        self.quick_speed = P[770]

        # 修改快速定位速度，降低回固定点速度
        P[770] = 2000 * (mm / minute)

        # 创建空的固定点位置列表
        self.fixed_point = []
        for i in range(basic.axisCount()):
            # 获取固定点位置初始值
            self.fixed_point.append(P[1601 + i])
            # 设置固定点位置
            P[1601 + i] = -0.001 * mm

    def tearDown(self):
        # 恢复快速定位速度初始值
        P[770] = self.quick_speed

        # 恢复固定点位置初始值
        for i in range(basic.axisCount()):
            P[1601 + i] = self.fixed_point[i]

    def test_回固定点(self):

        # 设置xyz运动的距离为行程的一半
        move_x = round((P[1501] + P[1521]) / 2)
        move_y = round((P[1502] + P[1522]) / 2)
        move_z = round((P[1503] + P[1523]) / 2)
        # XY轴先运动，Z轴再运动
        basic.mdi("G90 G53 G01 X{:.3f} Y{:.3f}".format(move_x / mm, move_y / mm))
        th.msleep(2000)
        basic.mdi("G90 G53 G01 Z{:.3f}".format(move_z / mm))
        th.msleep(3000)

        # 点击回固定点
        th.clickButton(basic.mainWindow, "回固定点")
        th.msleep(500)

        # 判断回固定点时“Z轴先抬高，XY轴不动
        assert (R[101] == round(move_x / BLU)) and (R[102] == round(move_y / BLU))
        for i in range(basic.spindleCount()):
            assert R[103 + i] != round(move_z / BLU)
        th.msleep(3000)

        # 判断回固定点时“Z轴回到固定点后，XY回再固定点”
        assert (R[101] != round(move_x / BLU)) and (R[102] != round(move_y / BLU))
        for i in range(basic.spindleCount()):
            assert R[103 + i] == round(-0.001 * mm / BLU)
        th.msleep(5000)

        # 判断XYZ轴是否都回到固定点
        assert (R[101] == round(-0.001 * mm / BLU)) and (R[102] == round(-0.001 * mm / BLU))
        for i in range(basic.spindleCount()):
            assert R[103 + i] == round(-0.001 * mm / BLU)
