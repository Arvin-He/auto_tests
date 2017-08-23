
import unittest
import testhelpers as th
import basic
import random
from plugins.mainui.mainwindow import _mainWindowContent


class MyTestCase(unittest.TestCase):

    def test_loadprogram(self):
        th.msleep(5000)
        basic.unloadProgram()
        th.msleep(2000)
        # 随机加载程序
        nclist = ["2013-5-30-3-样条曲线圆弧拟合.NC", "自动上下料(1)", "三维刀具半径补偿2.NC"]
        number = random.randint(0, len(nclist) - 1)
        nc = nclist[number]
        basic.loadProgram("E:/NC/%s" % (nc))
        th.msleep(2000)
        # 运行程序、停止
        basic.start()
        th.msleep(2000)
        basic.stop()
        th.msleep(1000)
        # 从断点行开始加工
        mainwindow = _mainWindowContent
        th.msleep(500)
        mainwindow.ui.tableView.slot_startFromBreakPoint()
        th.msleep(1000)
        basic.start()
        th.msleep(1000)
        basic.pause()
        th.msleep(1000)
        basic.stop()
