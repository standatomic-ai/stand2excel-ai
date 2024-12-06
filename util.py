# -*- encoding: utf-8 -*-
"""
@File    : util.py
@Time    : 2024/12/6 下午5:15
@Author  : HDK1999
@Email   : gg19990815@gmail.com
@Software: PyCharm
@Instructions: 工具链
"""
# 判断文件名是否在ai平台返回的列表中
def isInList(l, f):
    for i in l:
        if f is i.filename:
            return True,i.id
    return False,None