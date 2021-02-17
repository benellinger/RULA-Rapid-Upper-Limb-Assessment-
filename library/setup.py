    # -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 13:31:06 2015

@author: b.ellinger

This script converst a Python script to a *.exe using cx_freeze 4.3.4

To do so, follow these steps (in Power Shell):
I.  run: "python setup.py build"
II. For making plot-function working correctly several numpy *.dll files need to be imported to the *.exe folder.
    a. run: "cp %homepathPYTHON%\Lib\site-packages\numpy\core\mkl*.dll %homepath%\desired_EXE"
        e.g.:
        cp C:\WinPython-64bit-3.4.3.7\python-3.4.3.amd64\Lib\site-packages\numpy\core\mkl*.dll C:\_DATA\Kunden\OSP_Rheinland-Pfalz.Ullrich\application\v1.01\build\\exe.win-amd64-3.4
    b. run: "cp %homepathPYTHON%\Lib\site-packages\numpy\core\libiomp5md.dll %homepath%\desired_EXE"

    not sure how to do it with a MSI-installer
!!!Before doing so, be sure your script runs correctly!!!
"""

#
import cx_Freeze
import sys
import time
import numpy
import csv
import re

base = None

#if sys.platform == 'win32':
#    base = 'Win32GUI'

executables = [cx_Freeze.Executable('app.py', base=base, icon='rula.ico')]

packages = ['numpy', 'csv', 're', 'time', 'sys']

include_files = ['rula.ico']

cx_Freeze.setup(
    name = 'rula_velamed',
    options = {'build_exe': {'packages':packages,
        'include_files':include_files}},
    version = '0.11',
    description = 'rula velamed Applikation',
    executables = executables
    )
