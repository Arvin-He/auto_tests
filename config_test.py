
from PyQt5 import QtWidgets


def pytest_addoption(parser):
    parser.addoption(
        "--group", action="store", metavar="NAME", help="only run tests matching the group NAME.")


def pytest_configure(config):
    config.addinivalue_line("markers", "group(name): mark test to run only on named group")


def pytest_itemcollected(item):
    QtWidgets.qApp.processEvents()


def pytest_collection_modifyitems(items, config):
    selected = []
    deselected = []
    for item in items:
        groupmarker = item.get_marker("group")
        groupname = "" if groupmarker is None else groupmarker.args[0]
        option = item.config.getoption("--group")
        option = "" if option is None else option
        if groupname == option:
            selected.append(item)
        else:
            deselected.append(item)
    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = selected
