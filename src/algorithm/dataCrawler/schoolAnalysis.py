#coding=utf8
import login
import HTMLParser
import traceback
import html5lib
import urllib2
import httplib
import re
import bs4
import chardet
import cPickle
from debug import dprintf

def isSYSU(url):
    '''use urllib2 to get the data from url'''
    req = urllib2.Request(url=url,)
    text = ""
    try:
        result = urllib2.urlopen(req)
        encoding = result.headers.getparam('charset')
        text = result.read()
        chardet.detect(text)
        # text = text.decode(encoding).encode("utf-8")
    # except httplib.IncompleteRead as e:
    except Exception as e:
        print e
        # text = e.partial

    soup = bs4.BeautifulSoup(text)

    t = soup.select("script")
    s = ""
    for each in t:
        # grep the profile_info out
        if str(each).find('"pid":"pl_profile_hisInfo"') >0:
            s = str(each)
            break
    # if extract error, then regurn false
    if s == "":
        # dprintf("=============================\n" + url)
        print "extract error!"
        print url
        return False

    # parse the html code and escape the content
    start = s.find("html")
    start+=7
    end = s.find('"})</script')
    s = s[start:end]
    s = re.sub(r"\\\/","/", s)
    s = re.sub(r"\\t", "    ",s)
    s = re.sub(r"\\n", "\n",s)
    s = re.sub(r"&lt;", "<",s)
    s = re.sub(r"&gt;", ">",s)
    s = re.sub(r'\\"', '"',s)
    s = re.sub(r'&amp;', '&',s)

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
           
if __name__ == "__main__":
    client = login.APILogin()
    login.browserLogin();
    # test(1994626454,client)
    # test(1957829952,client)
    url = "http://weibo.com/1994626454"
    isSYSU(url)
