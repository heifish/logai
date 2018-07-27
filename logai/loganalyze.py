#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
日志分析模块
含有多种日志的分析函数

'''
import os,sys

import db2diag as _db2diag
import oraclealert as _oraclealert


def db2Analyze(logfile):
    ScriptPath = '\\'.join(logfile.split('\\')[:-1])
    logname = logfile.split('\\')[-1]
    os.chdir(ScriptPath)
    a = _db2diag.filterLogBlock(logname)
    print('logpath is %r,logname is %r'%(ScriptPath,logname))
    _db2diag.getInfo(logname,a)




def oraAnalyze(logfile,oraknowlib):
    ScriptPath = '\\'.join(logfile.split('\\')[:-1])
    logname = logfile.split('\\')[-1]
    os.chdir(ScriptPath)
    #获取错误日志对象列表
    oras = _oraclealert.findORA(logname)
    for ora in oras:
        for okl in oraknowlib:
            action = ora.findAction(okl)
            if action is not None:
                print('errnum is %r,errtime is %r, action is %r'%(ora.errnum,ora.errtimenum,action))



if __name__ == '__main__':
    ora_know = _oraclealert.OraKnowLib('D:\\projects\\logai\\logai\\knowlib\\oraclelib')
    oraknowlib = ora_know.getLibList()
    oraAnalyze('D:\\projects\\logai\\logai\\ftp\\1113天津滨海\\2018年6月\\10日\\数据库\\alert_netdb.log',oraknowlib)

