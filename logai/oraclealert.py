#!/usr/bin/python
# -*- coding: utf-8 -*-
'''


'''




import os ,sys
import time,re
import xlrd



class ErrLog():
    def __init__(self,errtimenum,errlinenum,errnum,errmessage):
        self.errtimenum = errtimenum
        self.errlinenum = errlinenum
        self.errnum = errnum
        self.errmessage = errmessage

    def findAction(self,oraknowlib):
        ken = oraknowlib['errnum'].split(',')
        for e in ken:
            #print('errlog errnum is %r,know errnum is %r'%(self.errnum,e))
            if self.errnum == e:
                return oraknowlib['action']
            else:continue
        return None


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
        "errnum":sht1.row_values(3)[3],
        "action":sht1.row_values(5)[1],
        "ItemName":sht1.row_values(1)[1],
        "FileName":file_name,
        "FilePath":"",
        "errmessage":sht1.row_values(4)[1],
        "reason":sht1.row_values(6)[1],
        "Prevent":sht1.row_values(7)[1],
        "Title":sht1.row_values(0)[1],
        "level":sht1.row_values(3)[1]
        }
        return row


def isValidDate(dateStr):
    try:
        time.strptime(dateStr, "%a %b %d %H:%M:%S %Y")
        return True
    except:
        return False


def findORA(filen):
    oralist = []
    with open(filen,'r',encoding="utf-8") as fo:
        logLines=enumerate(fo)
        errtimenum = 0
        for lineNum,logLine in logLines:
            if isValidDate(logLine[:24]):
                errtimenum = lineNum
            else:
                result = re.search('(^ORA-\d+)(.*)',logLine)
                if result is None:
                    continue
                else:
                    errnum = result.groups()[0]
                    errmessage = result.groups()[1]
                    errlog = ErrLog(errtimenum,lineNum,errnum,errmessage)
                    oralist.append(errlog)
    return oralist



if __name__ == '__main__':
    
    oras = findORA('alert_netdb.log')
    ora_know = OraKnowLib('D:\\projects\\logai\\logai\\knowlib\\oraclelib')
    oraknowlib = ora_know.getLibList()
    for ora in oras:
        for okl in oraknowlib:
            action = ora.findAction(okl)
            if action is not None:
                print('errnum is %r,errtime is %r, action is %r'%(ora.errnum,ora.errtimenum,action))
