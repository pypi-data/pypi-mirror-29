#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : log
# @Author : moridisa
# @Contact : moridisa@moridisa.cn
# @Date  : 2017/12/25

"""
make log and config log
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def set_log_level(level: int):
    loger = logging.getLogger()
    loger.setLevel(level)


def log(func):
    def wrapper(*args, **kwargs):
        f_name = func.__name__
        f_name = ' '.join(map(lambda x: x.capitalize(), f_name.split('_')))
        logging.info(f_name + ' --- Start')
        data = func(*args, **kwargs)
        logging.info(f_name + ' --- Done')
        return data

    return wrapper
