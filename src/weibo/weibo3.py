'''
Created on 2011-12-31
@author: cyb

Weibo Login.
'''
import httplib
import urllib
import urllib2, cookielib
import re
import time
import json
import hashlib
import gzip
import StringIO
#user: shuimu_88@163.com

class Weibo(object):
    def __init__(self):
        self.opener = None

    def hash_password(self, password, servertime, nonce):
        p = hashlib.sha1(password).hexdigest()
        p = hashlib.sha1(p).hexdigest() + str(servertime) + str(nonce)
        p = hashlib.sha1(p).hexdigest()
        return p
        
    def login(self):
        try:
            url1 = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=' + \
                  'sinaSSOController.preloginCallBack&su=c2h1aW11Xzg4JTQwMTYzLmNvbQ%3D%3D' + \
                  '&client=ssologin.js(v1.3.17)&_=' + str(time.time()).split('.')[0]
            url2 = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.17)'
            
            header1 = {
#                'Host': 'login.sina.com.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-cn,zh;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Charset': 'GB2312,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
                'Referer': 'http://weibo.com/'
            }
                 
            header2 = {
#                'Host': 'login.sina.com.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-cn,zh;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Charset': 'GB2312,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
                'Referer': 'http://weibo.com/',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            header3 = {
#                'Host': 'weibo.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-cn,zh;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Charset': 'GB2312,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
#                'Referer': url2
            }
            
            conn = httplib.HTTPConnection('login.sina.com.cn')
            conn.request('GET', url1, None, header1)
            resp1 = conn.getresponse()
            print resp1.status,resp1.reason
            hdoc = resp1.read()
            buf = StringIO.StringIO(hdoc)
            hdoc = gzip.GzipFile(fileobj=buf).read()
            print hdoc
            hdoc = hdoc.split('(')[1].split(')')[0]
            items = json.loads(hdoc)
            servertime = items['servertime']
            nonce = items['nonce']
            sp = self.hash_password('zcgyb0668', servertime, nonce)
            print sp
            
            postdata = {
                'entry': 'weibo',
                'gateway': '1',
                'from': '',  
                'savestate': '7',
                'useticket': '1',
                'ssosimplelogin': '1',
                'vsnf': '1',
                'vsnval': '',    
                'su': 'c2h1aW11Xzg4JTQwMTYzLmNvbQ==',
                'service': 'miniblog',
                'servertime': str(servertime),
                'nonce': nonce,
                'pwencode': 'wsse',
                'sp': sp,
                'encoding': 'UTF-8',
                'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                'returntype': 'META'
            }
            postdata = urllib.urlencode(postdata)
            conn.request('POST', url2, postdata, header2)
            resp2 = conn.getresponse()
            print resp2.status, resp2.reason
            data = resp2.read()
            buf = StringIO.StringIO(data)
            data = gzip.GzipFile(fileobj=buf).read()
            print data

            url3 = 'http://weibo.com/1789744932'
            conn2 = httplib.HTTPConnection('weibo.com')
            conn2.request('GET', url3, None, header3)
            resp3 = conn2.getresponse()
            print resp3.status, resp3.reason, resp3.getheaders()
            data = resp3.read()
            buf = StringIO.StringIO(data)
            data = gzip.GzipFile(fileobj=buf).read()
            print data

            f = open('foxxcyb.html', 'w')
            f.write(data)
            f.close()
            
        except urllib2.URLError, e:
            print e
    
    def open(self, url):
        try:
            fs = self.opener.open(url)
            return fs
        except Exception,e:
            print e
            return None

if __name__ == '__main__':
    weibo = Weibo()
    weibo.login()

