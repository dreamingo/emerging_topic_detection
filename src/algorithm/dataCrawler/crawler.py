#coding=utf8
import login
import HTMLParser
import traceback
import html5lib
import traceback
import urllib2
import httplib
import re
import bs4
import chardet
import cPickle
import time
import pymysql as MySQLdb
import configure
from debug import dprintf

MySQLdb.install_as_MySQLdb()
'''use urllib2 to get the data from url'''
def readText(url):
    req = urllib2.Request(url=url,)
    text = ""
    try:
        result = urllib2.urlopen(req)
        encoding = result.headers.getparam('charset')
        text = result.read()
        chardet.detect(text)
    except Exception as e:
        print e
    return text


'''Pharse_script in the html code '''
def pharse_script(text, scriptName):
    soup = bs4.BeautifulSoup(text)
    t = soup.select("script")
    s = ""
    for each in t:
        # if str(each).find('"pid":"pl_relation_hisFollow"') >=0:
        if str(each).find(scriptName) >=0:
            s = str(each)
            break
    # if extract error, then regurn false
    if s == "":
        print "extract error!"
        print url
        return s
    start = s.find("html")
    start+=7
    end = s.find('"})</script')
    s = s[start:end]
    #Escape the specify character
    s = re.sub(r"\\\/","/", s)
    s = re.sub(r"\\t", "    ",s)
    s = re.sub(r"\\n", "\n",s)
    s = re.sub(r"&lt;", "<",s)
    s = re.sub(r"&gt;", ">",s)
    s = re.sub(r'\\"', '"',s)
    s = re.sub(r'&amp;', '&',s)
    return s


'''Get the number of pages of one's friendList'''
def get_friends_pages(url):
    text = readText(url)
    s = pharse_script(text,'"pid":"pl_relation_hisFollow"')
    soup1=bs4.BeautifulSoup(s,"html5lib")
    pageList = soup1.find_all("a", {"action-type":"page"})
    if pageList:
        lastPage = re.findall('">(\d*)</a>', (str(pageList[-1])))[0]
        return int(lastPage)
    else:
        return 0

'''Crawer one's friends list id'''
def friend_crawler(id):
    url = "http://weibo.com/"+ id + "/follow?page=&page=" + str(1)
    pageNum = get_friends_pages(url)
    id_list = []
    for page in xrange(1, pageNum+1):
        url = "http://weibo.com/"+ id + "/follow?page=&page=" + str(page)
        text = readText(url)
        s = pharse_script(text, '"pid":"pl_relation_hisFollow"')
        soup1=bs4.BeautifulSoup(s,"html5lib")
        left = soup1.find_all("div", {"class":"left"})
        for i in left:
            id = re.findall('id=(\d*)', str(i))[0]
            id_list.append(id)

        print len(id_list)

def isSYSU(url):
    text = readText(url)
    s = pharse_script(text,'"pid":"pl_profile_hisInfo"')
    '''Get the info'''
    soup1=bs4.BeautifulSoup(s,"html5lib")
    infoTag = soup1.find_all("div", {"class":"tags"})
    title = re.findall('title=\"(.*)\"', str(infoTag))
    for i in title:
        chardet.detect(i)
        i = i.decode("utf-8").encode("utf-8")
        if i.find("中山大学") >= 0:
            return True
    return False
    

def test():
    conn = MySQLdb.connect(host='localhost', user='root',passwd='ddmbr')  
    cursor = conn.cursor()
    conn.select_db('ped')

    value = ['3','1234567', '2013-05-01', "我爱你"]
    cursor.execute("insert into weibo (id, userId, publish_time, content) values(%s, %s,%s,%s)",value )
    cursor.commit()

def pharse_data(date):
    data = date.split(" ")
    month = {'Jan': '01',
            'Feb':'02',
            'Mar':'03',
            'Apr':'04',
            'May':'05',
            'Jun':'06',
            'Jul':'07',
            'Aug':'08',
            'Sep':'09',
            'Oct':'10',
            'Nov':'11',
            'Dec':'12',
            }
    tmp_date = data[5] + '-' + month[data[1]] + '-' + data[2] + " " + data[3]
    return tmp_date

def data_store(weibo_data):
    data_ptr = open("../data/weibo_data", 'w')
    cPickle.dump(weibo_data, data_ptr)
    data_ptr.close()
    print "=============================="
    print "data_store complete!!"
    print "=============================="

def weiboCrawler():
    #get the API client
    client_id = 0
    client = login.APILogin((client_id) % configure.APP_COUNT)

    #connect the database
    #Get the users data
    user_ptr = open("../data/new_user", 'r')
    users = cPickle.load(user_ptr)
    weibo_data = []
    count = 0
    user_count = 4000
    #main_loop
    for user in users[4000::]:
        print "user_count", user_count
        user_count += 1
        try:
            uid = user['id']
            conn = MySQLdb.connect(host='localhost', user='root',passwd='ddmbr', db = 'ped', use_unicode=False)  
            cursor = conn.cursor()
            for i in xrange(1,3):
                weibos = client.get.statuses__user_timeline(count = 100, uid = uid, page = i)
                for weibo in weibos['statuses']:
                    count +=1
                    # weibo_data.append(weibo)
                    date = pharse_data(weibo['created_at'])
                    content = weibo['text'] 
                    if weibo.has_key("retweeted_status"):
                        content += '//'
                        content += weibo['retweeted_status']['text']
                    value = [weibo['mid'], uid, date, content.encode('utf-8')]
                    try:
                        cursor.execute("insert into weibo (mid, userId, publish_time, context) values(%s,%s,%s,%s)",value )
                        conn.commit()
                    except Exception as e:
                        print e
                print "count", count
            cursor.close()
            
        except Exception as e:
            print "================================="
            print "Exception !!!!!!!!!!!!!!!!!!!!!!!"
            print e
            print "================================="
            print traceback.print_exc()
            users.append(user)
            client_id += 1
            client = login.APILogin((client_id) % configure.APP_COUNT)
            print "change client to ", client_id % configure.APP_COUNT
            # data_store(weibo_data)
            time.sleep(100)
            
    # data_store(weibo_data)

if  __name__ == "__main__":
    # time.sleep(1000)
    weiboCrawler()
    # test()
    # pharse_data('Tue May 31 17:46:55 +0800 2011')
    # login.browserLogin();
    # id = "2003845811"
    # # url =  'http://weibo.com/1218025772/follow?page=&page=1'
    # tStart = time.time()
    # friend_crawler(id)
    # tEnd = time.time()
    # print tEnd - tStart




