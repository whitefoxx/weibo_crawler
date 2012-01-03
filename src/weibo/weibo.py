'''
Created on 2011-12-31
@author: cyb

Weibo Login.
'''
import urllib
import urllib2, cookielib
import re
import time
import json
import hashlib
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
            cookiejar = cookielib.LWPCookieJar()
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
            cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
            self.opener = urllib2.build_opener(cookie_support)
            urllib2.install_opener(self.opener)
            url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=' + \
                  'sinaSSOController.preloginCallBack&su=c2h1aW11Xzg4JTQwMTYzLmNvbQ%3D%3D' + \
                  '&client=ssologin.js(v1.3.17)&_=' + str(time.time()).split('.')[0]
            fs = self.opener.open(url)
            hdoc = fs.read()
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
            url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.17)'
            fs = self.opener.open(url, postdata)
            fs.close()
            
            f = open('foxxcyb.html', 'w')
            fs2 = self.opener.open('http://weibo.com/u/1789744932')
            f.write(fs2.read())
            fs2.close()
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

