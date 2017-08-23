#!/usr/bin/env python3

import os
import subprocess
import sys
import gevent
import gevent.socket

from _rpc import _eval, _exec

__dir__ = os.path.dirname(os.path.abspath(__file__))
_root_dir = __dir__
_test_helpers_dir = os.path.join(_root_dir, "test_helper")


def _connected():
    try:
        return _eval("0") == 0
    except (ConnectionResetError, gevent.Timeout):
        return False


def _wait_connected(timeout):
    # 等待  连接
    with gevent.Timeout(timeout):
        while not _connected():
            # print("等待  连接...")
            gevent.sleep(1)
    print("已连接")


def _wait_disconnected(timeout):
    # 等待  关闭
    with gevent.Timeout(timeout):
        while _connected():
            # print("等待  关闭...")
            gevent.sleep(1)
    print("已断开连接")


def _start():
    print("启动 ")
    if sys.platform == "win32":
        args = ["C:\\Python34\\python.exe", "F:\\-2.2\\run.py"]
    else:
        args = ["-admin", "start"]
    subprocess.Popen(args)
    _wait_connected(60)
    gevent.sleep(3)  # 等待开机动作执行结束


def _stop():
    print("关闭 ")
    _exec("closeApp()")
    _wait_disconnected(10)


def _restart():
    print("重启 ")
    _exec("rebootApp()")
    _wait_disconnected(10)
    _wait_connected(60)
    gevent.sleep(3)  # 等待开机动作执行结束


def _run_tests(args):
    print("执行测试", args)
    _exec("""\
import sys
if {0!r} not in sys.path:
    sys.path.insert(0, {0!r})
import testhelpers
run_tests({1!r})
""".format(_test_helpers_dir, args))
    # 等待测试执行完成
    while _eval("tests_running()", timeout=20):  # 测试收集过程可能卡住一段时间, 所以增加超时
        # print("等待测试执行完成...")
        gevent.sleep(1)
    print("测试执行完成")
    gevent.sleep(1)


def _main(args):
    if args:
        _run_tests(args)
        return

    # if not _connected():
    #     _start()

    _wait_connected(10)
    _run_tests(["-k", "功能测试"])

    # _restart()
    # _run_tests(["-k", "功能测试", "--group", "restart"])

    # _restart()
    # _run_tests(["-k", "功能测试", "--group", "restart again"])

    # gevent.sleep(3)

    # _stop()


if __name__ == "__main__":
    _main(sys.argv[1:])
