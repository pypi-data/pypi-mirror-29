# -*-coding:utf-8 -*-
from setuptools import setup

setup(
    name = "ttag",
    description = "translate original json data into the new json data",
    version = "0.4",
    author = "slc",
    author_email = "1427784107@qq.com",
    install_requires = [],
    packages = [
        "ttag"
    ],
    entry_points={
        "console_scripts":[
            'tprint=ttag.__init__:tprint',
            'ttrans=ttag.__init__:ttrans'
        ]
    }
)