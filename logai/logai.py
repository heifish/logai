'''
主程序逻辑：
    调用文件扫描模块，遍历ftp中对应日志文件夹，按照日志分类返回文件列表
    将读取的文件进行识别，不同日志文件调用不同模块进行分析
    ai分析模块根据规则筛选存在风险日志文件，调用知识库模块，匹配处理建议

文件扫描模块：
    遍历ftp中的文件夹，按照日志分类返回文件列表

ai分析模块：
    目前先做db2 数据库分析模块，筛选日志中的err信息，提取关键信息，NLTK,Pattern,langid.py,jieba,
    传递给知识库模块，进行匹配
    Numpy,scipy,Matplotlib,机器学习库,scikit-learn

知识库模块：
    传递进来关键信息，知识库名称，进行知识库遍历，匹配处理建议，并返回。如果未匹配到，
    提示发现新问题，转工程师处理，目前 知识库由各工程师维护，填写关键信息和处理建议
    #后期可以考虑，加入自我学习功能    

'''
import os ,sys

import re

from getfile import getDateFiles
import loganalyze
import oraclealert

class LogFile:
    def __init__(self,logpath):
        #路径含文件名
        self.log_fullpath = logpath
        self.log_path = logpath.split('\\')[:-1]
        self.log_name = logpath.split('\\')[-1]
        #print(self.log_name)

    def isOracle(self):
        ScriptPath = '\\'.join(self.log_path)
        os.chdir(ScriptPath)
        with open(self.log_name,'r',encoding="utf-8") as fo:
            line = fo.readline()
            
            while line:
                result = re.search('(LGWR switch)',line)
                if result is None:
                    line = fo.readline()
                    continue
                else:
                    return True
            
            return False

    def isDb2(self):
        ScriptPath = '\\'.join(self.log_path)
        os.chdir(ScriptPath)
        with open(self.log_name,'r',encoding="utf-8") as fo:
            line = fo.readline()
            
            while line:
                result = re.search('FUNCTION: DB2 UDB,',line)
                if result is None:
                    line = fo.readline()
                    continue
                else:
                    return True
            
            return False



    def getLogClas(self):
        '''
        如果没匹配返回None
        '''
        LogClas = {
        'db2':'db2diag.log',
        'oracle':'alert_netdb.log'
        }

        for k  in LogClas:
            if LogClas[k] == self.log_name:
                return k

        if self.isOracle():
            return 'oracle'
        elif self.isDb2():
            return 'db2'

        
        else:
            return None

    def analyze(self,logclas,knowlib):
        # logclas = self.getLogClas()  #自动检测自动分析
        if logclas == self.getLogClas():
            if logclas == 'db2':
                print('-------It is analyzing %r log %r------------'%(logclas,self.log_fullpath))
                loganalyze.db2Analyze(self.log_fullpath)

            elif logclas == 'oracle':
                print('-------It is analyzing %r log %r------------'%(logclas,self.log_fullpath))
                loganalyze.oraAnalyze(self.log_fullpath,knowlib)
            else:
                print('-log %r is not %r log,do not analyze-'%(self.log_fullpath,logclas))

        else:
            print('-log %r is not %r log,do not analyze-'%(self.log_fullpath,logclas))

           

#请求输入需要获取的日志期数
#sdate = input('请求输入需要获取的日志期数，类似610，625 [+]:')
sdate = 610
#对输入的内容进行排错处理

#定义ftp根目录
rootdir = r'D:\projects\logai\logai\ftp'
log_files = []

#获取日志文件集合
print('----正在获取日志列表----')
log_files = getDateFiles(rootdir,sdate)
print('----日志列表获取完成----')
print('log list is %r'%log_files)


#请求输入分析日志类别
#logclas = input('请输入想要分析的日志类别，类似 oracle , db2 [+]:')
logclas = 'oracle'

if logclas == 'oracle':
    ora_know = oraclealert.OraKnowLib('D:\\projects\\logai\\logai\\knowlib\\oraclelib')
    knowlib = ora_know.getLibList()
    print('---init ORACLELIB successful--')

for i in log_files:
    j = LogFile(i)
    j.analyze(logclas,knowlib)





