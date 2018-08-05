from urllib.request import urlopen,Request,urlparse,ProxyHandler,build_opener,install_opener
from urllib.error import URLError,HTTPError
#from UserAgent import mobileUserAgent,pcUserAgent
from datetime import datetime
import time
import re


# 分析目标，必应搜索
# 返回首页面链接



# <a target="_blank" href="
def get_links(html):
    # webpage_regex = re.compile('<h3>(.*?)</h3>')
    webpage_regex = re.compile('<h2><a target="_blank" href="(.*?)"')   # bing
    return webpage_regex.findall(html)

def download(url,proxy=None,user_agent='wswp',num_retries=2):
    print('[+] 正在下载: %s' % url)
    headers = { 'User-Agent':user_agent}
    req = Request(url, headers=headers)
    if proxy:
        handler = {urlparse(url).scheme:proxy}
        opener= build_opener(handler)
        install_opener(opener)
    try:
        # html = urlopen(req).read()
        html = urlopen(req).read().decode()
    except HTTPError as e:
        html = None
        print('[W] 下载出现服务器错误: %s' % e.reason)
        if num_retries > 0:
            print('[+] 尝试重新下载 第%d次' % (3 - num_retries))
            if hasattr(e,'code') and 500 <= e.code < 600:
                html = download(url,user_agent=user_agent,num_retries=num_retries-1)
        else:
            print('[E] 尝试重新下载失败')
    except URLError as e:
        html = None
        print("[E] 站点不可达: %s" % e.reason)
    return html

def webs(sk):

    # home_url = 'http://www.baidu.com/s?wd=%s'%sk

    home_url = 'https://cn.bing.com/search?q=%s'%sk
    # home_url = 'https://www4.bing.com/search?q=%s&FORM=BESBTB&ensearch=1'%sk
    print(sk)
    html = download(home_url)
    links = get_links(html)
    return links
    # print(html)
    # for link in get_links(html):
    #     # time.sleep(1)
    #     print(link)
if __name__ == '__main__':
     sk = 'ORA-12154' #要搜索的关键字
     webs(sk)
