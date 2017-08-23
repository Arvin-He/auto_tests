# !/user/bin/python
# -*- coding:utf-8 -*-
# @Author:Grace
import unittest
import random
import string
import basic
import gevent
# import testhelpers as th
from PyQt5 import QtCore, QtWidgets


class UserManager(unittest.TestCase):

    def test_UserManager(self):
        userData = basic.framData["userData"]
        from plugins.mainui.mainwindow import _mainWindowContent
        _mainWindowContent.ui.CF8.animateClick()
        gevent.sleep(1)
        dlg = basic.app.activeWindow()
        gevent.sleep(1)
        dlg.ui.CF7.animateClick()
        gevent.sleep(1)
        dlg2 = basic.app.activeWindow()
        gevent.sleep(1)
        dlg2.ui.operator_logion.animateClick()
        gevent.sleep(1)
        # 开发商登录
        from common.usermanagement.userlogiondialog import ShowUserlogiondialog
        QtCore.QTimer.singleShot(0, lambda: ShowUserlogiondialog("开发商", 0, True))
        gevent.sleep(0.5)
        dlg6 = basic.app.activeWindow()
        dlg6.ui.password.setText('GFDAUTO.COM')
        gevent.sleep(0.5)
        dlg6.ui.logion.animateClick()
        gevent.sleep(1)
        # 注销开发商登录
        dlg2.ui.cancellation.animateClick()
        gevent.sleep(1)
        dlg7 = basic.app.activeWindow()
        gevent.sleep(0.5)
        dlg7.buttons()[0].animateClick()
        gevent.sleep(1)

        dlg2.ui.operator_logion.animateClick()
        # 制造商
        QtCore.QTimer.singleShot(0, lambda: ShowUserlogiondialog("制造商", 5, True))
        gevent.sleep(0.5)
        dlg5 = basic.app.activeWindow()
        dlg5.ui.password.setText('051280988826')
        gevent.sleep(0.5)
        dlg5.ui.logion.animateClick()
        gevent.sleep(1)
        # 生成随机的密码
        str = string.digits + string.ascii_letters
        pwd = "".join(random.choice(str) for i in range(random.randint(8, 10)))
        print(pwd)
        # 从制造商权限修改技术员权限的密码
        dlg2.ui.technician_password.animateClick()
        gevent.sleep(1)
        dlg9 = basic.app.activeWindow()
        gevent.sleep(1)
        dlg9.ui.password.setText(pwd)
        gevent.sleep(1)
        dlg9.ui.confirm.setText(pwd)
        gevent.sleep(1)
        dlg9.ui.modify.animateClick()
        gevent.sleep(1)
        dlg10 = basic.app.activeWindow()
        gevent.sleep(1)
        dlg10.accept()
        gevent.sleep(3)
        dlg2.ui.operator_logion.animateClick()
        gevent.sleep(1)
        # 技术员
        dlg2.ui.technician_logion.animateClick()
        # QtCore.QTimer.singleShot(0, lambda: ShowUserlogiondialog("技术员", 15, True))
        gevent.sleep(1)
        dlg4 = basic.app.activeWindow()
        dlg4.ui.password.setText(pwd)
        gevent.sleep(0.5)
        dlg4.ui.logion.animateClick()
        gevent.sleep(2)
        # 机床厂
        # from common.usermanagement.userlogiondialog import ShowUserlogiondialog
        QtCore.QTimer.singleShot(0, lambda: ShowUserlogiondialog("机床厂", 10, True))
        gevent.sleep(0.5)
        dlg3 = basic.app.activeWindow()
        dlg3.ui.password.setText(userData[1]["password"])
        gevent.sleep(0.5)
        dlg3.ui.logion.animateClick()
        gevent.sleep(2)
        # dlg3.isShowPassWord = True
        # 登录机床厂之后，修改技术员密码不成功
        pwd2 = "".join(random.choice(str) for i in range(random.randint(8, 10)))
        gevent.sleep(1)
        dlg2.ui.technician_password.animateClick()
        gevent.sleep(1)
        dlg12 = basic.app.activeWindow()
        gevent.sleep(1)
        dlg12.ui.password.setText(pwd2)
        gevent.sleep(1)
        pwd3 = "".join(random.choice(str) for i in range(random.randint(8, 10)))
        dlg12.ui.confirm.setText(pwd3)
        gevent.sleep(1)
        dlg12.ui.modify.animateClick()
        gevent.sleep(1)
        dlg11 = basic.app.activeWindow()
        gevent.sleep(1)
        # ls1 = dlg11.findChildren(QtWidgets.QPushButton)
        dlg11.accept()
        # gevent.sleep(1)
        # dlg13 = basic.app.activeWindow()
        gevent.sleep(1)
        # print(dlg12)
        dlg12.reject()
        gevent.sleep(2)
        # 登录机床厂后，修改机床厂密码
        gevent.sleep(1)
        dlg2.ui.machine_password.animateClick()
        gevent.sleep(1)
        dlg8 = basic.app.activeWindow()
        print(dlg8)
        gevent.sleep(1)
        pwd1 = "".join(random.choice(str) for i in range(random.randint(8, 10)))
        dlg8.ui.origin_password.setText(userData[1]["password"])
        gevent.sleep(1)
        dlg8.ui.password.setText(pwd1)
        gevent.sleep(1)
        dlg8.ui.confirm.setText(pwd1)
        gevent.sleep(1)

        dlg8.ui.modify.setEnabled(True)
        dlg8.ui.modify.animateClick()
        gevent.sleep(1)
        dlg13 = basic.app.activeWindow()
        gevent.sleep(1)
        list = dlg13.findChildren(QtWidgets.QPushButton)
        list[0].click()
        gevent.sleep(1)
        dlg2.close()