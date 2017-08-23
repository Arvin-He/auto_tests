import unittest
import testhelpers as th
import basic
from basic import F, R
from common.manualoperation.manualoperation import ManualOpDialog
import random
import logging
from basic.unit import BLU
_logger = logging.getLogger(__name__)


class ManualBtn(unittest.TestCase):
    def setUp(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "手动")
        th.msleep(1000)
        self.win = th.assertActiveWindow(ManualOpDialog)

    def tearDown(self):
        th.close(self.win)

    def test_add(self):
        th.msleep(500)
        # self.assertTrue(self.win.isVisible())
        # add点击手动按钮
        button_list = self.win.buttons
        th.msleep(500)
        for i in ["0.01", "0.1", "1"]:
            th.clickButton(self.win, i)
            th.msleep(500)
            for btn in button_list:
                if btn == 0:
                    continue
                else:
                    th.click(widget=btn)
                    th.msleep(1000)
                    _logger.warning(str(tuple(round(R[341 + x] * BLU, 3) for x in range(basic.axisCount()))))
                    th.msleep(500)

        # 自定义模式点击手动按钮
        th.clickButton(ManualOpDialog, "自定义")
        th.msleep(500)
        lineEdit = self.win.ui.customstep
        th.lineEditTypewrite(
            str(random.randint(1, 20) + round(random.uniform(0.001, 1), 3)), lineEdit)
        th.msleep(500)
        for btn in button_list:
            th.click(widget=btn)
            th.msleep(1000)
            _logger.warning(str(tuple(round(R[341 + x] * BLU, 3) for x in range(basic.axisCount()))))
            th.msleep(500)

        # 连续模式点击手动按钮
        th.clickButton(ManualOpDialog, "连续")
        for btn in button_list:
            if btn == 0:
                continue
            else:
                th.click(widget=btn)
                th.msleep(1000)

        # 开启快动按钮点击手动按钮
        for btn in button_list:
            th.click(widget=btn)
            th.msleep(1000)
            _logger.warning(str(tuple(round(R[341 + x] * BLU, 3) for x in range(basic.axisCount()))))
            th.msleep(500)


def _hasHardLimit():
    ini = basic.sysData("ini/variable.in.ini")
    name = ini.get("X4", "zh_CN", fallback=None)
    return name is not None and name.startswith("限位-")
    print(name)


@unittest.skipIf(not _hasHardLimit(), "没有硬限位信号")
class limit_free(unittest.TestCase):
    def test_limit_free(self):
        # 将限位端口极性置为1
        th.msleep(2000)
        R[4240, 5] = True
        th.msleep(1000)
        # 点击limit_free
        R[1362, 1] = True
        th.msleep(1000)
        dlg = th.assertActiveWindow(ManualOpDialog)
        th.msleep(500)
        dlg.buttons[2].animateClick()
        th.msleep(1000)
        dlg.buttons[3].animateClick()
        th.msleep(1000)
        # 勾选硬限位时允许往限位方向运动
        R[233, 0] = True
        th.msleep(1000)
        dlg.buttons[1].animateClick()
        th.msleep(1000)
        dlg.buttons[2].animateClick()
        th.msleep(1000)
        # 将限位端口极性恢复成0
        R[4240, 5] = False
        th.msleep(1000)
        self.assertTrue(F[3])
        th.msleep(500)
        if F[3]:
            dlg.close()
        th.msleep(1000)
        self.assertFalse(dlg.isVisible())
