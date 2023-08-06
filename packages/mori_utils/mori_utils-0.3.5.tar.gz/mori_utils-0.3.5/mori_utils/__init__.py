#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : __init__
# @Author : moridisa
# @Contact : moridisa@moridisa.cn
# @Date  : 2017/12/21

import os

FILE_ROOT = os.getcwd()

from .logger import logging, log, set_log_level
from .data_operator import load_config, read_config, cache_returned
from .data_operator import query_mysql, execute_mysql, query_odps, query_mongo, get_mysql_db_name
from .net_works import invoke_dubbo, format_return_data, DubboParamInstance

try:
    load_config(os.path.join(FILE_ROOT, 'config'))
except Exception as e:
    logging.error('Mori Utils Can`t Load Config From: %s' % FILE_ROOT)

__all__ = [
    # static path
    'FILE_ROOT',

    # settings
    'load_config',
    'read_config',
    'set_log_level',

    # func wrapper
    'cache_returned',
    'log',

    # net work
    'invoke_dubbo',
    'DubboParamInstance',
    'format_return_data',

    # db
    'query_mysql',
    'execute_mysql',
    'query_odps',
    'query_mongo',
    'get_mysql_db_name',

    # module
    'logging',
]
