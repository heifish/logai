#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

'''

import os ,sys
import xlrd

ScriptPath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
os.chdir(ScriptPath)

#1、导入库关键信息用于匹配
#2、从AI传递的关键信息与获取的libKey进行匹配，并返回库文件名
def matchingkey(keyTag):
	fo=open("./db2LibFiles/db2FileKeys.lib","r",encoding='utf-8')
	for keyRow in fo:
		if keyTag in keyRow:
			return(eval(keyRow)['fName'])
	fo.close()

if __name__ == "__main__":
	matchingkey("hadr")