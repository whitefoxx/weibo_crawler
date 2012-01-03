#! -*- encoding:utf-8 -*-
import StringIO
import gzip
import urllib2
import re

"""
    Weibo account: shuimu_88@163.com
"""
cookie = 'SUS=SID-1789744932-1325485823-JA-ab6v3-825d71755a572f8423b7abbd7a8674b4; SUE=es%3D0c9e0ff431d182656f826475eb0dfa43%26ev%3Dv1%26es2%3D152ef8d9ca7753718fc83db371ee72ff%26rs0%3DDgKaAcjk3lwVy5kPC5dnIiNo3YUrEtWRRtvJ2JPNAzFWIEw3u3hX%252FbvwWNCJnEeyPICk%252B9J0ZjSup9vVgqJCOL%252B%252FUFztxT69u7gTnqHx7pxkM7CypI5pQF7ah71N5GvK6F4lPsvD44JkS8p%252FcdyezraMt8yyU5MsB%252B397U2LRUo%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1325485823%26et%3D1325572223%26d%3Dc909%26i%3D13b0%26us%3D1%26uid%3D1789744932%26user%3Dshuimu_88%2540163.com%26ag%3D4%26name%3Dshuimu_88%2540163.com%26nick%3Dguge%26fmp%3D%26lcp%3D2011-08-04%252015%253A41%253A22%26vf%3D0%26ac%3D2; ALF=1326090618; SSOLoginState=1325485823; wvr=3.6; USRHAJAWB=usrmdins13121; un=shuimu_88@163.com; USRHAWB=usrmdins212_542; ads_ck=1; _s_tentry=weibo.com; UOR=weibo.com,weibo.com,; Apache=8430538139278.456.1325485892311; SINAGLOBAL=8430538139278.456.1325485892311; ULV=1325485892540:1:1:1:8430538139278.456.1325485892311:'
headers = {
    'Host': 'weibo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-cn,zh;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Charset': 'GB2312,utf-8;q=0.7,*;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'http://weibo.com/',
    'Cookie': cookie
}

def str2real_unicode(s):
    return eval("u'" + s + "'")

def get_response_data(url):
    req = urllib2.Request(url, None, headers)
    res = urllib2.urlopen(req)
    data = res.read()
    buf = StringIO.StringIO(data)
    data = gzip.GzipFile(fileobj=buf).read()
    return data

def transform(filepath):
    if filepath.endswith(".r"):
        f = open(filepath, 'r')
        data = f.read()
        f.close()
        if filepath.endswith(".info.r"):
            index1 = data.find('</body>')
            data = data[data.find('<div', index1):data.find('pl_content_hisFans', index1)]
        data = data.replace('\n','')
        data = data.replace('\\/','/')
        data = data.replace('\'', r'\'')
        data = str2real_unicode(data)
        f = open(filepath[:-2] + '.t', 'w')
        f.write(data)
        f.close()
        
def get_weibo(weibo_id, last_id):
    buf = ''
    page = 1
    for page in range(1,6):
        url = 'http://weibo.com/aj/mblog/mbloglist?page=%d&count=15&pagebar=0&uid=%s&_t=0' % (page, weibo_id)
        data = get_response_data(url)
        data = data[data.find('"data":"')+8:-2].strip()
        if data.find('feed_list_item') == -1:
            break
        index1 = data.find(r'mid=\"') + 6
        index2 = data.find(r'\"', index1)
        mid = int(data[index1:index2])
        # increment crawl
        if mid <= last_id:
            break
        buf += data
        if page == 1:
            max_id = mid
        
        url = 'http://weibo.com/aj/mblog/mbloglist?page=%d&pre_page=%d&count=15&pagebar=0&uid=%s&_t=0' % (page, page, weibo_id)
        data = get_response_data(url)
        data = data[data.find('"data":"')+8:-2].strip()
        if data.find('feed_list_item') == -1:
            break
        index1 = data.find(r'mid=\"') + 6
        index2 = data.find(r'\"', index1)
        mid = int(data[index1:index2])
        # increment crawl
        if mid <= last_id:
            break
        buf += data
        
        url = 'http://weibo.com/aj/mblog/mbloglist?page=%d&pre_page=%d&count=15&pagebar=1&uid=%s&_t=0' % (page, page, weibo_id)
        data = get_response_data(url)
        data = data[data.find('"data":"')+8:-2].strip()
        if data.find('feed_list_item') == -1:
            break
        index1 = data.find(r'mid=\"') + 6
        index2 = data.find(r'\"', index1)
        mid = int(data[index1:index2])
        # increment crawl
        if mid <= last_id:
            break
        buf += data
    
    f = open('./data/' + weibo_id + '_' + str(max_id) + '.weibo.r','w')
    f.write(buf)
    f.close()    
    return max_id

def parse_weibo(weibo_id):
    pass

def get_info(weibo_id):
    url = 'http://weibo.com/%s/info' % weibo_id
    data = get_response_data(url)
    f = open('./data/' + weibo_id + '.info.r','w')
    f.write(data)
    f.close()
    
def parse_info(weibo_id):
    filepath = './data/' + weibo_id + '.info.t'
    f = open(filepath, 'r')
    buf = f.read()
    f.close()
    i1 = buf.find('"html":"<dl>')
    i2 = buf.find('</dl>', i1)
    profile = buf[i1:i2]
    p1 = re.compile(r'<strong>([\w\W]+?)</strong>')
    p2 = re.compile(r'<dd>([\w\W]+?)</dd>')
    p3 = re.compile(r'>([\w\W]+?)<')
    cs = p1.findall(profile)
    ds = p2.findall(profile)
    ss = []
    for d in ds:
        s = ''
        ts = p3.findall(d)
        for t in ts:
            if t.strip() and not t.endswith('：'):
                s += t + ','
            elif t.strip():
                s += t
        s = re.sub('\n|\t| ','',s)
        ss.append(s)
    
    info = {}
    i = 0
    for c in cs:
        if c == '基本信息':
            info['base'] = ss[i]
        elif c == '教育信息':
            info['edu'] = ss[i]
        elif c == '工作信息':
            info['work'] = ss[i]
        i += 1
    print info
#            print t.replace('\n', '').strip()
#        print re.sub(r'<[\w\W]+?>','',d).strip()

    
def url_test(url):
    data = get_response_data(url)
    f = open('homepage.html', 'w')
    f.write(data)
    f.close()
    return
    data = data[data.find('"data":"')+8:-2].strip()
    if data.find('feed_list_item') != -1:
        data = data.replace('\\/','/')
        data = data.replace('\'', r'\'')
        data = str2real_unicode(data)
        f = open('url_test.html', 'w')
        f.write(data)
        f.close()
       
if __name__ == '__main__':
#    max_id = get_weibo('diaoyifu', 3387987704806394)
#    print max_id
#    parser('diaoyifu')
    #url_test('http://weibo.com/diaoyifu/info')
#    get_info('diaoyifu')
#    transform('./data/' + 'diaoyifu.info.r')
    parse_info('diaoyifu')
    
