
'''
search ftp dir ,find all log file

getDateFiles(ftphomedir,sdate)
sdate-->give date director,example 610, or 625
search from ftp home director, subdir project name ,subdir year and mouth ,subdir is date, subdir is log class 

return -->file list . like ['D:\\projects\\logai\\logai\\1113天津滨海\\2018年6月\\10日\\交换机\\switchlog.txt', 'D:\\projects\\logai\\logai\\1113天津滨海\\2018年6月\\10日\\数据库\\db2diag.log']


'''

import os ,sys

#正式用函数
def getDateFiles(directory,sdate):
    files_list = []  #遍历的文件列表
    re_files = []   #返回的文件列表
    sdate = str(sdate)
    sm = sdate[:-2]  #月份
    sd = sdate[-2:]  #日期
    sm = '2018年'+sm+'月'
    sd = sd + '日'

    for root,sub_dirs,files in os.walk(directory):
        for special_file in files:
            files_list.append(os.path.join(root,special_file))
    #print(directory)
    for sf in files_list:
        #拆分sf字符串，取得具体月份sfm，具体日期sfd
        sf_path = sf.split('\\')
        for sfm in sf_path:
            for sfd in sf_path:
                if sm == sfm and sd == sfd:
                    re_files.append(sf)
                    #print('find a match file %s' %sf)
                    break

            
    return re_files


if __name__ == '__main__':
    rootdir = r'D:\projects\logai\logai\ftp'
    print(rootdir)
    teststr = getDateFiles(rootdir,610)
    print('%r' %teststr)