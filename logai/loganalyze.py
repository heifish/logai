#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
日志分析模块
含有多种日志的分析函数

'''
import os,sys

# import db2diag as _db2diag
import oraclealert


# def db2Analyze(logfile):
#     ScriptPath = '\\'.join(logfile.split('\\')[:-1])
#     logname = logfile.split('\\')[-1]
#     os.chdir(ScriptPath)
#     a = _db2diag.filterLogBlock(logname)
#     print('logpath is %r,logname is %r'%(ScriptPath,logname))
#     _db2diag.getInfo(logname,a)




def oraAnalyze(logfile,oraknowlib):
    # ScriptPath = '\\'.join(logfile.split('\\')[:-1])
    # logname = logfile.split('\\')[-1]
    # os.chdir(ScriptPath)
    #获取错误日志对象列表
    errlog = oraclealert.ErrLog(logfile)
    errlog.doIt(oraknowlib)
    filename = logfile + 'analyze.txt'
    # print(filename,logfile)
    with open(filename,'w',encoding='utf-8') as fw:
        for i in range(len(errlog.errlist)) :
            line = '''
Find err %r:
The last error time is %r 
The error message is %r
Action is %r
            '''%(i+1 ,errlog.errlist[i]['last_errtime'] ,errlog.errlist[i]['errmessage'] ,errlog.actionlist[i])
            fw.write(line)
    print('====Analyzed file is %r'%filename)


if __name__ == '__main__':
    ora_know = _oraclealert.OraKnowLib('D:\\projects\\logai\\logai\\knowlib\\oraclelib')
    oraknowlib = ora_know.getLibList()
    oraAnalyze('D:\\projects\\logai\\logai\\ftp\\1113天津滨海\\2018年6月\\10日\\数据库\\alert_netdb.log',oraknowlib)

