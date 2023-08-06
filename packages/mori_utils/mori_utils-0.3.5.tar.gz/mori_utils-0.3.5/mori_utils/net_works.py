#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : net_works
# @Author : moridisa
# @Contact : moridisa@moridisa.cn
# @Date  : 2017/12/21

"""
网络相关的东西

some thing with net work
"""

import re
import json
import logging
import telnetlib
from typing import Iterable, Dict, Tuple
from .data_operator import get_zookeeper_host
from kazoo.client import KazooClient

brackets_match = re.compile('\(|\)')
__decode_fmt__ = 'gbk'


def set_dubbo_decode(decode: str):
    global __decode_fmt__
    __decode_fmt__ = decode


def format_return_data(data: Iterable, count: int = None, msg: str = None, status: bool = True) -> Dict:
    """
    格式化报文

    format response message

    :param data: 数据
    :param count: 数据长度
    :param msg: 消息
    :param status: 状态
    """
    data = {
        'count': len(list(data)),
        'status': 'Success' if status is True else 'Fail',
        'data': data
    }
    if count:
        data['count'] = count
    if msg:
        data['msg'] = msg
    return data


def __write_to_dubbo__(tn: telnetlib.Telnet, cmd: str):
    decode_cmd = cmd.encode(__decode_fmt__)
    decode_cmd += b'\n'
    logging.info(decode_cmd)
    tn.write(decode_cmd)


def __read_from_dubbo__(tn: telnetlib.Telnet):
    total_content = tn.read_until('dubbo>'.encode(__decode_fmt__), 2).decode(__decode_fmt__)
    total_content = total_content.split('dubbo>')[0]
    return total_content.split('elapsed:')[0]


def __read_dubbo_host_port__(service: str, config_name: str) -> Tuple[str, str]:
    """
    从zookeeper 获取 dubbo地址和端口 --- author: Tatum (塔叔❤️)

    read host and prot for dubbo from zookeeper --- author: Tatum (塔叔❤️)

    :param service: 服务名
    :param config_name: 配置名
    :return: 地址, 端口
    """
    zk = KazooClient(hosts=get_zookeeper_host(config_name))
    zk.start()
    providers_node = '/dubbo/{0}/providers'.format(service)
    providers = zk.get_children(providers_node)
    zk.stop()
    zk.close()
    if len(providers) == 0:
        raise Exception('None service found')
    provider = providers[0]
    m = re.match(r'dubbo%3A%2F%2F(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})%3A(?P<port>[0-9]{1,5})%2F.*',
                 provider)
    return m.group('host'), m.group('port')


class DubboParamInstance:
    """
    dubbo 接口传递对象
    """

    def __init__(self, class_name: str, **kwargs):
        """
        创建一个dubbo中的接口需要的对象参数

        create a instance for dubbo api instance param

        :param class_name: 参数类名
        :param kwargs: 参数值
        """
        self.param = {'class': class_name}
        self.param.update(kwargs)

    def __str__(self):
        return json.dumps(self.param)


def invoke_dubbo(service: str, method: str, config_name: str, args: Iterable, decode_charset='gbk'):
    """
    调用dubbo 接口

    call dubbo api

    :param service: 服务
    :param method: 方法
    :param config_name: 配置名
    :param decode_charset: 解码方式
    :param args: 参数(目前还不支持按名赋值)
    :return: 结果
    """
    # telnet connect to dubbo service
    host, port = __read_dubbo_host_port__(service, config_name)
    tn = telnetlib.Telnet(host=host, port=int(port))

    # send command line
    __write_to_dubbo__(tn, f'ls -l {service}')

    # read from telnet
    content = __read_from_dubbo__(tn)
    target_method_info = next(filter(lambda x: ' ' + method + '(' in x, content.split('\r\n')))
    pure_args_for_method = re.sub(r'\(|\)', '', target_method_info.split(method)[1]).split(',')

    default_args = []
    args_string_indexs = []
    for index, i in enumerate(pure_args_for_method):
        if i == 'java.lang.String':
            default_args.append(''),
            args_string_indexs.append(index)
        elif i == 'int':
            default_args.append(0),
        elif i == 'boolean':
            default_args.append('true')
        elif i == 'double' or i == 'float':
            default_args.append(0.0)
        elif '[]' in i:
            default_args.append([])
        else:
            default_args.append('null')

    args = list(args)
    if len(args) != len(default_args):
        raise ValueError(f'Args length is not match expectation: {len(default_args)} parameters')
    for i in range(len(default_args)):
        if args[i] is None:
            args[i] = default_args[i]
        elif isinstance(args[i], bool):
            args[i] = 'true' if args[i] else 'false'
    formated_args = ','.join([f'"{x}"' if args.index(x) in args_string_indexs else str(x) for x in args])
    __write_to_dubbo__(tn, f'invoke {service}.{method}({formated_args})')
    result = __read_from_dubbo__(tn)
    try:
        return json.loads(result, encoding=decode_charset)
    except Exception as e:
        logging.error(e)
        return result
