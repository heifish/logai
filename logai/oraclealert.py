#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
筛选出错误日志
同一时间的日志所有ORA-组成一个识别码，去匹配知识库里面的识别码，知识库的识别码是一个字符串，拆分成列表
遍历日志列表，拿一个日志块字典，以index遍历知识库列表，日志中的识别码是一个列表，遍历他，去判断是否in 知识库的识别码列表，
匹配一个计数+1，如果计数==日志识别码长度，为全部匹配，计数>0，就可以记录知识库索引号。返回所有匹配的索引号index
根据索引号返回知识库内容，全部匹配放到第一位

先不考虑自学习，

'''




import os ,sys
import time,re
import xlrd
import operator
from webs import webs


def isValidDate(dateStr):
    try:
        time.strptime(dateStr, "%a %b %d %H:%M:%S %Y")
        return True
    except:
        return False



#错误日志类，errtimnum是错误日志断的发生时间，errlinenum是错误日志的错误所在行，errnum是错误号ORA-11021这样的，errmessage是错误信息,flag标识是否多个错误号,默认0单个
class ErrLog():
    '''
    log1 = ErrLog("alert_netdbtest.log")
    log1.doIt(okllist)

    '''
    def __init__(self,filen):
        self.file = filen
        self.oralist = None
        self.errlist = None
        self.actionlist = None
        # self.errlist = []  # 元素为字典，key有errcount，lasterrtime，errnum()，errmessage()  使用函数_errlist初始化
        # self.actionlist = [] # 元素为字符串，与errlist一一对应  使用函数findaction初始化

    def doIt(self,okllist):
        self.oralist = self.findORA()
        self.errlist = self.errList(self.oralist)
        self.actionlist = self.findAction(okllist)
        # if self.actionlist not is None:
        #     return

    # 对日志进行分析，筛选出单错误日志段，对类中errlist进行一次初始化
    def findORA(self):
        '''
        返回错误日志块，# 没有去重的错误列表,元素是列表[errtimenum,errtime,errnum[],errmessage[]]
        没有报错返回空列表
        读取文件失败，返回None

        '''
        oralist = [] 
        tpl = [0,'',set(),[]]
        iserr = False
        errtimenum = 0
        with open(self.file,'r',encoding="utf-8") as fo:
            logLines=enumerate(fo)

            for lineNum,logLine in logLines:
                # 查找时间的行，记录errtimenum
                if isValidDate(logLine[:24]):
                    # 行号从0开始初始化
                    if lineNum > errtimenum and iserr:
                        oralist.append(tpl)
                        tpl = [0,'',set(),[]]
                    errtimenum = lineNum
                    errtime = logLine[:24]
                    iserr = False

                else:
                    result = re.search('(^ORA-\d+)(.*)',logLine)
                    # 查找以ORA-开头的行
                    # 错误代码ORA-28391
                    if result is None:
                        continue
                    else:
                        errnum = result.groups()[0]
                        while len(errnum) < 9:
                            _ten = errnum[4:]
                            errnum = 'ORA-' + '0' + _ten
                        # 错误代码之后的信息
                        # errmessage = result.groups()[1]
                        errmessage = result.groups()  #整行信息
                        iserr = True
                        tpl[0] = errtimenum
                        tpl[1] = errtime
                        tpl[2].add(errnum)
                        tpl[3].append(errmessage)


            return oralist  #如果为空[]，则没有查到错误

        return None  #打开文件失败

    def errList(self,oralist):
        '''# 元素为字典，key有errcount，last_errtime，errnum()，errmessage()  使用函数_errlist初始化
            oralist 元素是列表[errtimenum,errtime,errnum[],errmessage[]]
            返回字典列表err_list


        '''
        errlist = []
        tpd = {}
        if oralist is None:
            print('open file failed!')
        elif len(oralist) == 0:
            print('not find ora error in file ')
        else:
            tp_errnum_list = [] # 处理过的错误集合
            for ora in reversed(oralist):  #反向迭代，取最后的错误时间
                if ora[2] not in tp_errnum_list:
                    tp_errnum_list.append(ora[2])
                    errlist.append({'last_errtime':ora[1],'errnum':ora[2],'errmessage':ora[3]})
        return errlist

    def findAction(self,okllist):
        # okllist 知识库字典组成的列表,
        actionlist = []
        for err in self.errlist: 
            eaction = [] #针对本地遍历错误的解决方案
            # eadvise = []
            n = [] #匹配到的知识库的索引
            for i in range(len(okllist)):
                oranum = okllist[i]['errnum'].split(',')
                if operator.eq(err['errnum'],oranum):
                    n.append(i)
                for e in err['errnum'] :
                    if e in oranum:
                        n.append(i)
            if len(n) == 0:
                s = []
                for e in err['errnum']:
                    s.append(webs(e))
                notfind = ('%r not find action in knowlib,find is on www from bing %r'%(err['errnum'],s))
                # t = (notfind,'Ask you enniger')
                eaction.append(notfind)
            else:
                for i in range(len(n)):
                    ok = okllist[n[i]]
                    eaction.append(ok['action'])
                    # eadvise.append(ok['advise'])
            
            actionlist.append(eaction)

        return actionlist








        

class OraKnowLib():
    def __init__(self,knowpath):
        self.knowpath = knowpath

    #遍历库目录，生成包含库信息字典的列表
    def getLibList(self):
        libList = []
        os.chdir(self.knowpath)
        for file_name in os.listdir(self.knowpath):
            if ".xls" in file_name:
                row=self.__getLibDict(file_name)
                libList.append(row)
        return libList

    #读取库文件，生成包含库信息的字典
    def __getLibDict(self,file_name):
        shts = xlrd.open_workbook(file_name)#当前打开的表格
        sht1 = shts.sheet_by_index(0)#当前表格的第一个sheet
        row={
        "errnum":sht1.row_values(3)[3], # 错误代码
        "action":sht1.row_values(5)[1], # 建议处理方法
        "ItemName":sht1.row_values(1)[1],
        "FileName":file_name,
        "FilePath":"",
        "errmessage":sht1.row_values(4)[1], # 错误信息
        "reason":sht1.row_values(6)[1], # 原因
        "advise":sht1.row_values(7)[1], # 建议 ignore action
        "Title":sht1.row_values(0)[1],
        "level":sht1.row_values(3)[1]
        }
        return row




