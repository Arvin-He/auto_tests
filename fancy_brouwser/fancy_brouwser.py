#!/usr/bin/env python3
import os
import sys
_pyqt5_dir = "C:\\Python34\\Lib\\site-packages\\PyQt5"
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(_pyqt5_dir, "plugins")
_fancybrowser_dir = os.path.join(_pyqt5_dir, "examples\\webkit\\fancybrowser")
sys.path[0] = _fancybrowser_dir
if len(sys.argv) > 1:
    sys.argv[1] = "file:///" + os.path.abspath(sys.argv[1])
exec(open(os.path.join(_fancybrowser_dir, "fancybrowser.py")).read())
