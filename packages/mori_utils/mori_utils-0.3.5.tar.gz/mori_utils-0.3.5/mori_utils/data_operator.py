#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : data_operator.py
# @Author : moridisa
# @Contact : moridisa@moridisa.cn
# @Date  : 2017/12/21

"""
all data operation
"""

import os
import odps
import yaml
import pickle
import pymysql
import pymongo
import logging
from typing import List, Iterable, Callable, Dict, Any
from pymysql.connections import Connection
from pymongo import MongoClient
from . import FILE_ROOT

__GLOBAL_CONFIGS__ = {}
CACHES_PATH = os.path.join(FILE_ROOT, 'caches')
if os.path.exists(CACHES_PATH) is False:
    os.mkdir(CACHES_PATH)


def cache_returned(prefix: str = None,
                   suffix: str = None,
                   rename: str = None,
                   cache_by: Iterable = None,
                   is_log: bool = True):
    """
    缓存函数返回值(适用于结果比较固定的函数)

    cache func returned data

    :param func: callable func
    :return: func()
    """

    def wrapper(func: Callable):
        def _f_wrapper_(*args, **kwargs):
            func_name = f'{func.__module__}.{func.__name__}' if rename is None else rename
            if prefix:
                func_name = f'{prefix}_{func_name}'
            if suffix:
                func_name = f'{func_name}_{suffix}'
            if cache_by is not None:
                if args is not None:
                    args_name = '_'.join(map(lambda x: str(args[x]), cache_by))
                    func_name = f'{func_name}_by_{args_name}'
                elif kwargs is not None:
                    kwargs_name = '_'.join(map(lambda x: str(kwargs[x]), cache_by))
                    func_name = f'{func_name}_by_{kwargs_name}'
                else:
                    raise TypeError('support cache args/kwargs by int/str')
            func_name = func_name.replace('/', '_')
            cache_file_path = os.path.join(CACHES_PATH, f'{func_name}.cache.pickle')
            if os.path.exists(cache_file_path):
                data = pickle.load(open(cache_file_path, 'rb'))
                if is_log:
                    logging.info(f'load data from cache for {func_name}')
            else:
                data = func(*args, **kwargs)
                pickle.dump(data, open(cache_file_path, 'wb'))
                if is_log:
                    logging.info(f'save data to cache for {func_name}')
            return data

        return _f_wrapper_

    return wrapper


def load_config(root_path: str):
    """
    加载配置路径

    load all config files

    :param root_path: 根目录
    """

    for file in filter(lambda x: x.endswith('.yaml'), os.listdir(root_path)):
        logging.info('Read Config From config, %s' % file)
        config = yaml.load(open(os.path.join(root_path, file), 'r'))
        __GLOBAL_CONFIGS__.update(config)


def read_config(config_name: str) -> Dict:
    """
    从__GLOBAL_CONFIGS__读取配置

    read config from __GLOBAL_CONFIGS__

    :param config_name: 配置名称
    :return: Dict 配置
    """
    if config_name not in __GLOBAL_CONFIGS__:
        raise IndexError
    else:
        return __GLOBAL_CONFIGS__[config_name]


def __get_odps_connection__(config_name: str) -> odps.ODPS:
    """
    生成odps链接对象

    make odps connection instance

    :param config_name: config name
    :return: odps connection_instance
    """
    config = __GLOBAL_CONFIGS__[config_name]
    return odps.ODPS(config['access_key_id'], config['access_key_secret'], config['project_name'], config['end_point'])


def __get_mysql_connection__(config_name: str) -> Connection:
    """
    链接数据库, 构建链接对象

    load mysql config & make a mysql connection

    :param config_name: 配置名
    """
    if config_name in __GLOBAL_CONFIGS__:
        config = __GLOBAL_CONFIGS__[config_name]
        conn = pymysql.connect(**config)
    else:
        raise Exception('Db Not in Config')
    return conn


def __get_mongo_connection__(config_name: str) -> MongoClient:
    """
    链接mongo

    connection to mongo

    :param config_name: 配置名
    :return: mongo 客户端
    """
    config = __GLOBAL_CONFIGS__[config_name]
    client = pymongo.MongoClient('mongodb://' + config['host'])
    client[config['auth']].authenticate(config['username'], config['password'])
    return client


def query_mongo(config_name: str, condition: dict, collection_name: str = None) -> Iterable:
    """
    查询mongo

    query on mongo

    :param config_name: 配置名
    :param condition: 查询条件
    :param collection_name: 指定collection
    :return:
    """
    config = __GLOBAL_CONFIGS__[config_name]
    with __get_mongo_connection__(config_name) as mongo_client:
        db = mongo_client.get_database(config['db'])
        collection = db.get_collection(
            collection_name if collection_name is not None else config['collection'])
        cursor = collection.find(condition)
        for result in cursor:
            yield result
        cursor.close()


def query_odps(config_name: str, sql: str, use_dict: bool = False) -> Iterable:
    """
    查询 odps

    query on odps

    :param config_name: 配置名
    :param sql: 查询语句
    :param use_dict: 使用字典做为返回值
    :return: 查询结果生成器
    """
    instance = __get_odps_connection__(config_name)
    with instance.execute_sql(sql).open_reader(use_tunnel=True, limit_enabled=False) as reader:
        if use_dict:
            for record in reader:
                yield dict(record)
        else:
            for record in reader:
                yield record.values


def query_mysql(config_name: str, sql: str, use_dict: bool = False) -> List:
    """
    查询mysql

    query on mysql

    :param config_name: 配置名
    :param sql: sql语句
    :param use_dict: 使用字典作为返回值类型
    :return: 查询结果
    """
    conn = __get_mysql_connection__(config_name)
    with conn:
        if use_dict:
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        else:
            cursor = conn.cursor()
        with cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
    return result


def get_mysql_db_name(config_name: str) -> str:
    """
    获取mysql中的数据库名

    get mysql db name in config

    :param config_name:
    :return:
    """
    return __GLOBAL_CONFIGS__[config_name]['db']


def execute_mysql(config_name: str, sql: str) -> int:
    """
    执行mysql 语句

    :param config_name: 配置名
    :param sql: sql
    :return: 如果是insert 返回id, 其他的返回受影响的行数
    """
    conn = __get_mysql_connection__(config_name)
    with conn:
        cursor = conn.cursor()
        with cursor:
            effect_row = cursor.execute(sql)
            if sql.lower().startswith('insert'):
                effect_row = cursor.lastrowid
        conn.commit()
    return effect_row


def get_zookeeper_host(config_name: str) -> str:
    """
    生成zookeeper url

    get zookeeper host

    :param config_name: 配置名
    :return: zookeeper 地址
    """
    return __GLOBAL_CONFIGS__[config_name]['keeper_list'].split(',')[0]
