#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

'''

import os ,sys
import xlrd

ScriptPath = os.path.split( os.path.realpath( sys.argv[0] ) )[0]
os.chdir("%s\\db2libFiles"%ScriptPath)

#遍历库目录，生成库关键词文件
def genLibFiles():
	fo = open("db2FileKeys.lib","a",encoding='utf-8')
	for file_name in os.listdir("."):
		if ".xls" in file_name:
			row=genLibKey(file_name)
			fo.writelines(str(row)+"\n")
			fo.close()

#读取库文件关键词，返回dict，包含文件名与关键词
def genLibKey(file_name):
	sheets_temp = xlrd.open_workbook(file_name)#当前打开的表格
	sheets_temp_1 = sheets_temp.sheet_by_index(0)#当前表格的第一个sheet
	keys=sheets_temp_1.row_values(3)[3]
	row={"fName":ScriptPath+"\\db2libFiles\\"+file_name,"keys":keys}
	return row

if __name__ == "__main__":
	genLibFiles()