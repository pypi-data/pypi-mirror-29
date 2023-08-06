# -*-coding:utf-8 -*-
from setuptools import setup

setup(
    name = "scantask",
    description = "create/delete new scantask",
    version = "0.1",
    author = "slc",
    author_email = "1427784107@qq.com",
    install_requires = [
       'elasticsearch >= 5.0.0'
    ],
    packages = [
        "scantask"
    ],
    entry_points={
        "console_scripts":[
            'scan_task=scantask.__init__:scan_task'
        ]
    }
)