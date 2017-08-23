#!/user/bin/env python3
# @Author: Grace
import unittest
import basic
from basic import R, P
from basic.unit import mm, minute, BLU
import testhelpers as th


class BackWPHome(unittest.TestCase):

    def setUp(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        # 获取快速定位速度
        self.quick_speed = P[770]
        # 修改快速定位速度，降低BackWPHome速度
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

    def test_BackWPHome(self):
        # 设置xyz运动的距离为行程的一半
        move_x = round((P[1501] + P[1521]) / 2)
        move_y = round((P[1502] + P[1522]) / 2)
        move_z = round((P[1503] + P[1523]) / 2)

        # XY轴先运动，Z轴再运动
        basic.mdi("G90 G00 X{:.3f} Y{:.3f}".format(move_x / mm, move_y / mm))
        th.msleep(8000)
        basic.mdi("G90 G53 G00 Z{:.3f}".format(move_z / mm))
        th.msleep(3000)

        # 点击BackWPHome
        th.clickButton(basic.mainWindow, "BackWPHome")
        th.msleep(500)
        # Z工件坐标
        wcs_z = round(move_z / BLU - R[143])
        # 判断BackWPHome时“Z轴先抬高，XY轴不动
        assert (R[121] == round(move_x / BLU)) and (R[122] == round(move_y / BLU))
        for i in range(basic.spindleCount()):
            assert R[123 + i] != wcs_z
        th.msleep(3000)

        # Z工件坐标原点
        wcs_origin_z = round(R[103] - R[143])
        # 判断BackWPHome时“Z轴回到工件原点后，XY回再工件原点”
        assert (R[121] != round(move_x / BLU)) and (R[122] != round(move_y / BLU))
        for i in range(basic.spindleCount()):
            assert R[123 + i] == wcs_origin_z
        th.msleep(6000)

        # 判断XYZ轴是否都回到工件原点
        assert (R[121] == 0) and (R[121] == 0)
        for i in range(basic.spindleCount()):
            assert R[123 + i] == wcs_origin_z
