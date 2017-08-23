#!/user/bin/env python3
# @Author: Grace
import unittest
import testhelpers as th
import basic
from basic import F
from PyQt5 import QtWidgets
import string
import random


class Tool(unittest.TestCase):

    def setUp(self):
        th.msleep(1000)
        th.assertActiveWindow(basic.mainWindow)
        th.msleep(500)
        # 打开刀具页面
        th.clickButton(basic.mainWindow, "刀具")
        self.tool = th.assertActiveWindow(basic.ToolDialog)
        th.msleep(500)
        # 创建空刀具名称列表，保存刀具列表原始值
        self.list_name = []
        self.table = self.tool.findChildren(QtWidgets.QTableWidget)
        for i in range(self.table[0].rowCount()):
            self.list_name.append(self.table[0].item(i, 2).text())
        # 点击刀具全选，完成测试初始化设置
        th.clickButton(self.tool, "全选")
        th.msleep(500)

    def tearDown(self):
        th.close(self.tool)

    def test_Tool(self):
        # 加载测试程序
        basic.loadProgram("E:/NC/自动测试程序/分别外形尺寸补偿功能测试程序.NC")
        th.msleep(500)
        th.close(self.tool)
        th.msleep(500)
        # 判断刀具全部勾选
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(1000)
        assert basic.GetMainToolNo() == 1
        th.msleep(8000)
        assert basic.GetMainToolNo() == 2
        th.msleep(3000)
        assert basic.GetMainToolNo() ==3
        th.msleep(3000)
        assert F[3]

        # 判断未勾选任何刀具
        th.clickButton(basic.mainWindow, "刀具")
        tool = th.assertActiveWindow(basic.ToolDialog)
        th.msleep(500)
        th.clickButton(tool, "反选")
        th.msleep(500)
        th.close(tool)
        th.msleep(500)
        th.clickButton(basic.mainWindow, "F11开始")
        th.msleep(1000)
        # 如果弹出Qmessagebox则没有勾选任何刀具
        msg = th.assertActiveWindow(QtWidgets.QMessageBox)
        th.clickButton(msg, "取消")

        # 在刀具名称那一栏输入值
        th.clickButton(basic.mainWindow, "刀具")
        th.msleep(500)
        # print(table[0].item(0, 2).text())
        th.clickButton(self.tool, "全选")
        th.msleep(500)
        # 定义包含所有数字，字母和特殊字符的字符串
        s1 = string.digits + string.ascii_letters + '~{}!@#$%^&*()><?-+='
        # 随机给刀具名称列表输入值
        for i in range(self.table[0].rowCount()):
            text = "".join(random.choice(s1) for j in range(10,30))
            self.table[0].item(i,2).setText(text)
        th.msleep(1000)
        # 判断输入的字符串有没有保存
        # assert self.list_name[i] != table[0].item(i,2).text()
        th.msleep(500)
        # 卸载NC程序
        basic.unloadProgram()
        th.msleep(1000)
        basic.loadProgram("E:/NC/自动测试程序/2013样条曲线圆弧拟合.NC")
        th.msleep(1000)
        basic.unloadProgram()
        th.msleep(1000)
        basic.loadProgram("E:/NC/自动测试程序/分别外形尺寸补偿功能测试程序.NC")
        # 刀具半径只可输入数字不可输入字符串
        for i in range(self.table[0].rowCount()):
            num = str(round(random.uniform(0, 1000), 3))
            self.table[0].item(i,4).setText(num)
        th.msleep(1000)

        for i in range(self.table[0].rowCount()):
            text = "".join(random.choice(s1) for j in range(5, 15))
            self.table[0].item(i, 5).setText(text)
        th.msleep(1000)

        # 刀具寿命
        th.msleep(500)
        th.lineEditTypewrite("10", tool.findChild(QtWidgets.QLineEdit,"toolmaxlife"))
        th.msleep(500)
        th.lineEditTypewrite("5", tool.body.currentWidget().ui.toolcurrentlifez)
