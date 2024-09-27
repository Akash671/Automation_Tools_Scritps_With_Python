# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 13:20:35 2023

@author: akash
"""

import sys
import os
from cx_Freeze import setup, Executable

# Get the ABSOLUTE path to the PyQt5 plugins directory
import PyQt5
plugins_path = os.path.join(os.path.dirname(PyQt5.__file__), 'Qt', 'plugins')
absolute_plugins_path = os.path.abspath(plugins_path) #Get absolute path

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base)]

setup(
    name="Keysight Tools",
    version="1.0",
    description="ATT/TMO Batch Downloader",
    options={
        "build_exe": {
            "packages": ["requests", "PyQt5", "os", "sys", "threading"],
            "include_files": [
                (absolute_plugins_path, 'c:/Users/Administrator/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0/LocalCache/local-packages/Python311/site-packages/PyQt5'), #Use absolute path here
                os.path.join(absolute_plugins_path, 'imageformats'), #If needed
                # Add other plugins if necessary
            ],
            "include_msvcr": True,
        }
    },
    executables=executables
)

#open cmd and enter below command
#python main.py build