
import unittest
import testhelpers as th
import basic
from basic import R, F, P
from common.parameters.param_dialog import ParamsDialog
from common.coordinate.coordinatedialog import CoordinateDialog
from common.simu3d.simu3d_dialog import Simu3dDialog
from PyQt5 import QtWidgets
from basic.unit import BLU, mm


class 程序开始时检查是否对刀(unittest.TestCase):

    def setUp(self):
        for a in range(basic.axisCount()):
            R[641 + a] = 1
        basic.Set_Auth_Level(0)

    def test_程序开始时检查是否对刀(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "参数")
        th.msleep(1000)
        dlg = th.assertActiveWindow(ParamsDialog)
        th.msleep(500)
        P[4006] = 1
        th.msleep(500)
        dlg.close()
        th.msleep(500)
        for i in range(basic.spindleCount()):
            R[31, i] = 0
        th.msleep(1000)
        basic.start()
        th.msleep(2000)
        self.assertTrue(F[3])
        th.msleep(500)
        P[4006] = 0
        th.msleep(1000)
        basic.start()
        th.msleep(2000)
        self.assertFalse(F[3])
        th.msleep(500)
        basic.stop()
        th.msleep(2000)
        self.assertTrue(F[3])


class 坐标清零需要确认(unittest.TestCase):
    def setUp(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "坐标设定")
        th.msleep(1000)
        self.win = th.assertActiveWindow(CoordinateDialog)

    def tearDown(self):
        th.close(self.win)

    def test_坐标清零需要确认(self):
        P[2506] = 1
        th.msleep(500)
        th.findButtons(self.win, "清零")
        buttons = th.findButtons(self.win, "清零")
        for i in buttons:
            th.click(widget=i)
            th.msleep(1500)
            msg = th.assertActiveWindow(QtWidgets.QMessageBox)
            th.clickButton(msg, "确定")
            th.msleep(1000)
            th.click(widget=i)
            th.msleep(1500)
            msg = th.assertActiveWindow(QtWidgets.QMessageBox)
            th.clickButton(msg, "取消")
            th.msleep(500)
        P[2506] = 0
        th.msleep(500)
        th.findButtons(self.win, "清零")
        buttons = th.findButtons(self.win, "清零")
        for i in buttons:
            th.click(widget=i)
            th.msleep(1500)
            th.assertActiveWindow(CoordinateDialog)
        th.msleep(1000)


class 启用多坐标系(unittest.TestCase):
    def setUp(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "坐标设定")
        th.msleep(1000)
        self.win = th.assertActiveWindow(CoordinateDialog)

    def tearDown(self):
        th.close(self.win)

    def test_启用多坐标系(self):
        th.msleep(500)
        # 勾选“使用多坐标系”
        P[4305] = 1
        th.msleep(1000)
        # # 设置每个坐标系的工件坐标和材料厚度
        lineEdit_x = self.win.ui.offset_x
        lineEdit_y = self.win.ui.offset_y
        thickness = self.win.ui.groupBox_4.findChildren(QtWidgets.QLineEdit)
        th.msleep(1000)
        offsetx = 160
        offsety = -160
        for wcs in ["G54", "G55", "G56", "G57", "G58", "G59"]:
            offsetx = offsetx - 10
            offsety = offsety + 10
            th.clickButton(self.win, wcs)
            th.lineEditTypewrite(str(offsetx), lineEdit_x)
            th.lineEditTypewrite(str(offsety), lineEdit_y)
            for i in thickness:
                th.lineEditTypewrite("-50", i)
            th.msleep(1000)
        th.close(self.win)
        th.msleep(1000)
        self.win = th.assertActiveWindow(basic.mainWindow)
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/多坐标系.NC")
        th.msleep(2000)
        # 进行仿真
        th.clickButton(basic.mainWindow, "仿真")
        th.msleep(1000)
        self.win = th.assertActiveWindow(Simu3dDialog)
        th.moveTo(widget=self.win.ui.widget)
        th.msleep(1000)
        th.rightClick()
        th.msleep(1000)
        th.assertActiveMenu()
        th.clickMenu("俯视图")
        th.msleep(1000)
        th.rightClick()
        th.msleep(1000)
        th.assertActiveMenu()
        th.clickMenu("标尺")
        self.win = th.assertActiveWindow(Simu3dDialog)
        th.clickButton(self.win, "连续仿真")
        th.msleep(1000)
        # 输出仿真图形
        th.screenshot()
        th.msleep(1000)
        # 关闭仿真对话框
        th.close(self.win)
        # # 取消勾选“使用多坐标系”
        P[4305] = 0
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "坐标设定")
        th.msleep(1000)
        self.win = th.assertActiveWindow(CoordinateDialog)
        self.assertTrue(self.win.ui.G54.isEnabled())
        self.assertFalse(self.win.ui.G55.isEnabled())


class 加工结束后动作(unittest.TestCase):
    def setUp(self):
        th.startSetup()
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/自动上下料(1)")

    def test_加工结束后动作(self):
        # 加工结束后回固定点
        P[4001] = 0
        th.msleep(500)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(35000)
        # 判断机床坐标等于固定点参数值
        for i in range(basic.axisCount()):
            assert (round(R[101 + i] * BLU) == P[1601 + i] * mm)
        th.msleep(500)
        # 加工结束后回工件原点
        P[4001] = 1
        th.msleep(500)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(35000)
        # 判断X,Y工件坐标等于0，Z轴机床坐标等于固定点参数值
        assert (R[121] == R[122] == 0)
        for a in range(basic.spindleCount()):
            assert round(R[103 + a] * BLU) == P[1603 + a] * mm
        # 加工结束后无附件动作
        P[4001] = 2
        th.msleep(500)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(35000)
        # 判断X，Y，Z工件坐标等于NC程序最后的X，Y，Z走的值
        assert round(R[121] * BLU) == 0 * mm and round(R[122] * BLU, 3) == -62.375 * mm
        for b in range(basic.spindleCount()):
            assert round(R[123 + b] * BLU) == 5 * mm


class 暂停时停转主轴(unittest.TestCase):
    def setUp(self):
        th.startSetup()
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/兰亭集序.NC")

    def tearDown(self):
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")

    def test_暂停时停转主轴(self):
        P[4002] = 1
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(6000)
        for i in range(basic.spindleCount()):
            # 判断主轴已启动且同步
            assert F[71 + i] and F[81 + i]
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "暂停")
        th.msleep(5000)
        assert F[1]
        # 判断主轴未启动且同步
        for i in range(basic.spindleCount()):
            assert not F[71 + i] and F[81 + i]
        # 判断主轴转速为0
        for i in range(basic.spindleCount()):
            assert R[191 + i] == 0
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "停止")
        P[4002] = 0
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(6000)
        # 判断主轴已启动且同步
        for i in range(basic.spindleCount()):
            assert F[71 + i] and F[81 + i]
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "暂停")
        th.msleep(5000)
        assert F[1]
        # 判断主轴已启动且同步
        for i in range(basic.spindleCount()):
            assert F[71 + i] and F[81 + i]


class 停止时停转主轴(unittest.TestCase):
    def setUp(self):
        th.startSetup()
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/兰亭集序.NC")

    def test_停止时停转主轴(self):
        P[4100] = 1
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(6000)
        # 判断主轴已启动且同步
        for i in range(basic.spindleCount()):
            assert F[71 + i] and F[81 + i]
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(5000)
        assert F[3]
        # 判断主轴未启动且同步
        for i in range(basic.spindleCount()):
            assert not F[71 + i] and F[81 + i]
        # 判断主轴转速为0
        for i in range(basic.spindleCount()):
            assert R[191 + i] == 0
        P[4100] = 0
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(6000)
        # 判断主轴已启动且同步
        for i in range(basic.spindleCount()):
            assert F[71 + i] and F[81 + i]
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(5000)
        assert F[3]
        # 判断主轴已启动且同步
        for i in range(basic.spindleCount()):
            assert F[71 + i] and F[81 + i]


class 暂停时抬刀(unittest.TestCase):
    def setUp(self):
        th.startSetup()
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/兰亭集序.NC")

    def tearDown(self):
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")

    def test_暂停时抬刀(self):
        P[4008] = 1
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(3000)
        # 判断Z轴机床坐标不为0
        for i in range(basic.spindleCount()):
            assert round(R[103 + i] * BLU) != 0 * mm
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "暂停")
        th.msleep(200)
        assert F[1]
        # 判断Z轴进给速度不为0
        for i in range(basic.spindleCount()):
            R[173 + i] != 0
        th.msleep(6000)
        # 判断Z轴机床坐标为0
        for i in range(basic.spindleCount()):
            assert round(R[103 + i] * BLU) == 0 * mm
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(1000)
        P[4008] = 0
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(5000)
        # 判断Z轴机床坐标不为0
        for i in range(basic.spindleCount()):
            assert round(R[103 + i] * BLU) != 0 * mm
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "暂停")
        th.msleep(500)
        assert F[1]
        # 判断Z轴进给速度为0且机床坐标不为0
        for i in range(basic.spindleCount()):
            assert R[173 + i] == 0 and round(R[103 + i] * BLU) != 0 * mm


class 停止时抬刀(unittest.TestCase):
    def setUp(self):
        th.startSetup()
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/兰亭集序.NC")

    def test_停止时抬刀(self):
        P[4101] = 1
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(5000)
        # 判断Z轴机床坐标不为0
        for i in range(basic.spindleCount()):
            assert round(R[103 + i] * BLU) != 0 * mm
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(200)
        assert F[3]
        # 判断Z轴进给速度不为0
        for i in range(basic.spindleCount()):
            R[173 + i] != 0
        th.msleep(6000)
        # 判断Z轴机床坐标为0
        for i in range(basic.spindleCount()):
            assert round(R[103 + i] * BLU) == 0 * mm
        th.assertActiveWindow(basic.mainWindow)
        th.msleep(1000)
        P[4101] = 0
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(5000)
        # 判断Z轴机床坐标不为0
        for i in range(basic.spindleCount()):
            assert round(R[103 + i] * BLU) != 0 * mm
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(500)
        assert F[3]
        # 判断Z轴进给速度为0且机床坐标不为0
        for i in range(basic.spindleCount()):
            assert R[173 + i] == 0 and round(R[103 + i] * BLU) != 0 * mm


class 操作员禁用暂停停止功能(unittest.TestCase):

    def setUp(self):
        th.startSetup()
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/兰亭集序.NC")

    def test_操作员禁用暂停停止功能(self):
        P[4142] = 1
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "其他功能")
        th.msleep(1000)
        # self.win = th.assertActiveWindow(basic.otherDialog)
        # 登录操作员
        self.win = QtWidgets.QApplication.activeWindow()
        if self.win.windowTitle() == "其他功能":
            th.clickButton(self.win, "用户管理")
            self.win = th.assertActiveWindow(basic.UserManagementDialog)
            th.clickButton(self.win, "操作员登录")
        th.msleep(500)
        th.close(self.win)
        th.msleep(1000)
        assert basic.Auth_Level() == 20
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(5000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "暂停")
        win = QtWidgets.QApplication.activeWindow()
        assert win.windowTitle() == "用户登录"
        th.msleep(1000)
        # 输入技术员密码，登录技术员
        th.typewrite("051280988566")
        th.msleep(500)
        th.press('enter')
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "暂停")
        th.msleep(500)
        # 判断为进给保持状态
        assert F[1]
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(1000)
        # 判断为准备好状态
        assert F[3]
        # 再次登录操作员
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "其他功能")
        self.win = QtWidgets.QApplication.activeWindow()
        if self.win.windowTitle() == "其他功能":
            th.clickButton(self.win, "用户管理")
            self.win = th.assertActiveWindow(basic.UserManagementDialog)
            th.clickButton(self.win, "操作员登录")
        th.msleep(500)
        th.close(self.win)
        assert basic.Auth_Level() == 20
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(5000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        win = QtWidgets.QApplication.activeWindow()
        assert win.windowTitle() == "用户登录"
        th.msleep(1000)
        th.typewrite("051280988566")
        th.msleep(500)
        th.press('enter')
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(1000)
        # 判断为准备好状态
        assert F[3]
        P[4142] = 0
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "其他功能")
        self.win = QtWidgets.QApplication.activeWindow()
        if self.win.windowTitle() == "其他功能":
            th.clickButton(self.win, "用户管理")
            self.win = th.assertActiveWindow(basic.UserManagementDialog)
            th.clickButton(self.win, "操作员登录")
        th.msleep(500)
        th.close(self.win)
        th.msleep(1000)
        assert basic.Auth_Level() == 20
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(5000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "暂停")
        th.msleep(1000)
        # 判断为进给保持状态
        assert F[1]
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(3000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(1000)
        # 判断为准备好状态
        assert F[3]


class 操作员禁用坐标设定(unittest.TestCase):

    def test_操作员禁用坐标设定(self):
        P[4143] = 1
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "其他功能")
        th.msleep(1000)
        # self.win = th.assertActiveWindow(basic.otherDialog)
        # 登录操作员
        self.win = QtWidgets.QApplication.activeWindow()
        if self.win.windowTitle() == "其他功能":
            th.clickButton(self.win, "用户管理")
            self.win = th.assertActiveWindow(basic.UserManagementDialog)
            th.clickButton(self.win, "操作员登录")
            th.msleep(500)
            th.close(self.win)
            th.msleep(1000)
            assert basic.Auth_Level() == 20
            th.assertActiveWindow(basic.mainWindow)
            th.clickButton(basic.mainWindow, "坐标设定")
            th.msleep(1000)
            th.assertActiveWindow(basic.mainWindow)
            P[4143] = 0
            th.clickButton(basic.mainWindow, "坐标设定")
            th.msleep(1000)
            win = th.assertActiveWindow(CoordinateDialog)
            th.close(win)


class 安全高度(unittest.TestCase):

    def setUp(self):
        th.startSetup()
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/自动上下料(1)")

    def test_安全高度(self):
        P[4005] = 40
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(5000)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")
        th.msleep(500)
        # 清空仿真图形
        th.clickButton(basic.mainWindow, "仿真")
        th.msleep(1000)
        win = th.assertActiveWindow(Simu3dDialog)
        th.moveTo(widget=win.ui.widget)
        th.msleep(1000)
        th.rightClick()
        th.msleep(1000)
        th.assertActiveMenu()
        th.clickMenu("清空")
        th.msleep(500)
        th.close(win)
        th.msleep(1000)
        # 从断点行开始加工
        th.moveTo(widget=th._mainWindowContent.ui.tableView)
        th.msleep(500)
        th.rightClick()
        th.msleep(500)
        th.assertActiveMenu()
        th.clickMenu("从断点行开始加工")
        th.msleep(500)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(3000)
        # 查看仿真图形
        th.clickButton(basic.mainWindow, "仿真")
        th.msleep(1000)
        win = th.assertActiveWindow(Simu3dDialog)
        th.moveTo(widget=win.ui.widget)
        th.msleep(1000)
        # 切换到前视图
        th.rightClick()
        th.msleep(1000)
        th.assertActiveMenu()
        th.clickMenu("前视图")
        th.msleep(1000)
        # 打开标尺
        win = th.assertActiveWindow(Simu3dDialog)
        win.ui.widget.m_isRuler = True
        th.msleep(1000)
        # 输出仿真图形
        th.screenshot()
        th.msleep(1000)
        # 关闭仿真对话框
        th.close(win)
        th.assertActiveWindow(basic.mainWindow)
        th.clickButton(basic.mainWindow, "F12 停止")


class 过切检查误差(unittest.TestCase):

    def setUp(self):
        th.startSetup()
        # 加载NC程序
        th.loadProgram("E:/NC/自动测试程序/五角星过切.nc")

    def test_过切检查误差(self):
        P