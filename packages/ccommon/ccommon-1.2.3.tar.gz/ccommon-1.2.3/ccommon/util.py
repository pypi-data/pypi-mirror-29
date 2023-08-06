#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/21 14:20
# @Author  : chenjw
# @Site    : 
# @File    : util.py
# @Software: PyCharm Community Edition
# @Desc    :  do what

import time
import decimal

# 获取当天时间
def zeroStr(added=0):
    '''
    :param added: offset,最好是 86400 的整倍数
    :return: 返回时间 like ‘2018-01-01’
    '''
    return time.strftime('%Y-%m-%d', time.localtime(time.time() + added))

def round(f,r):
    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
    b = decimal.Decimal('%s'%(f), decimal.getcontext())
    return float(b.__round__(r))

if __name__ == '__main__':
    pass
