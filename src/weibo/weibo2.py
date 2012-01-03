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
            cookiejar = cookielib.MozillaCookieJar()
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
#            cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
#            self.opener = urllib2.build_opener(cookie_support)
            self.opener.addheaders = [('User-agent', 'Opera/9.23')]
            urllib2.install_opener(self.opener)
            url1 = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=' + \
                  'sinaSSOController.preloginCallBack&su=c2h1aW11Xzg4JTQwMTYzLmNvbQ%3D%3D' + \
                  '&client=ssologin.js(v1.3.17)&_=' + str(time.time()).split('.')[0]
            url2 = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.17)'
            
            header1 = {
                #'Host': 'login.sina.com.cn',
                'Host': 'weibo.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-cn,zh;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Charset': 'GB2312,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
                'Referer': 'http://weibo.com/',
                'Cookie': 'SUS=SID-1789744932-1325485823-JA-ab6v3-825d71755a572f8423b7abbd7a8674b4; SUE=es%3D0c9e0ff431d182656f826475eb0dfa43%26ev%3Dv1%26es2%3D152ef8d9ca7753718fc83db371ee72ff%26rs0%3DDgKaAcjk3lwVy5kPC5dnIiNo3YUrEtWRRtvJ2JPNAzFWIEw3u3hX%252FbvwWNCJnEeyPICk%252B9J0ZjSup9vVgqJCOL%252B%252FUFztxT69u7gTnqHx7pxkM7CypI5pQF7ah71N5GvK6F4lPsvD44JkS8p%252FcdyezraMt8yyU5MsB%252B397U2LRUo%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1325485823%26et%3D1325572223%26d%3Dc909%26i%3D13b0%26us%3D1%26uid%3D1789744932%26user%3Dshuimu_88%2540163.com%26ag%3D4%26name%3Dshuimu_88%2540163.com%26nick%3Dguge%26fmp%3D%26lcp%3D2011-08-04%252015%253A41%253A22%26vf%3D0%26ac%3D2; ALF=1326090618; SSOLoginState=1325485823; wvr=3.6; USRHAJAWB=usrmdins13121; un=shuimu_88@163.com; USRHAWB=usrmdins212_542; ads_ck=1; _s_tentry=weibo.com; UOR=weibo.com,weibo.com,; Apache=8430538139278.456.1325485892311; SINAGLOBAL=8430538139278.456.1325485892311; ULV=1325485892540:1:1:1:8430538139278.456.1325485892311:'
            }
            
            
                 
            header2 = {
                'Host': 'login.sina.com.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-cn,zh;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Charset': 'GB2312,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
                'Referer': 'http://weibo.com/',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': '378'
            }
            
            header3 = {
                'Host': 'weibo.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-cn,zh;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Charset': 'GB2312,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
                'Referer': url2
            }
            
            req1 = urllib2.Request('http://weibo.com/whitefoxx', None, header1)
            #self.opener.open('http://weibo.com/')
            #req1 = urllib2.Request('http://')
            fs = self.opener.open(req1)
#            fs = urllib2.urlopen(req1)

            hdoc = fs.read()
            print hdoc
            return
#            buf = StringIO.StringIO(hdoc)
#            f = gzip.GzipFile(fileobj=buf)
#            hdoc = f.read()
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
            req2 = urllib2.Request(url2, postdata)
            fs = self.opener.open(req2)
#            fs = urllib2.urlopen(req2)
            print fs.read()
            fs.close()
            print cookiejar
            req3 = urllib2.Request('http://weibo.com/u/1789744932?wvr=3.6&lf=reg')
            f = open('foxxcyb.html', 'w')
            fs2 = self.opener.open(req3)
#            fs2 = urllib2.urlopen(req3)
            f.write(fs2.read())
            fs2.close()
            f.close()
            
            print cookiejar
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

