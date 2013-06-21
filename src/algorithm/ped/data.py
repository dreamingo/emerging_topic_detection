#encoding=utf-8
import marshal
import pymysql as MySQLdb
import datetime
import cPickle

STORE_DIR = 'tmp_data/hours/'
T = 10
t = 2
DAYS = False
initTime = datetime.datetime(2013,05,01,0,0,0)

#initailization of the mysqldb
MySQLdb.install_as_MySQLdb()
conn = MySQLdb.connect(host='localhost', charset='utf8', user='root',passwd='1', db = 'ped_new', use_unicode=False )   
# conn = MySQLdb.connect(host='localhost', user='root',passwd='1', db = 'ped', charset='utf8')   
cursor = conn.cursor()

corpus = [] #The ith set in the list represent the TWt(the corpus in interval i)
weiboVector = []  #the ith list in the list represent the vetors of the tweet in interval i
nutrition = [] #the ith dict in the list represent the nuturition of each term at interval i
energy = [] #the ith dict in the list represent the nuturition of each term at interval i
# topics = [] #the ith set in the list represent the topics at interval i
contentEnergy = []

# get the user authority
users_ptr = open('../data/backup/new_user', 'r')
users = cPickle.load(users_ptr)
users_ptr.close()
authority = {user['idstr']:user['authority'] for user in users}

#get the stop words list
stopWordsPtr = open('tmp_data/new_stopwords.txt', 'r')
stopWord = set([line.split('\n')[0].decode('utf-8') for line in stopWordsPtr.readlines()])
stopWordsPtr.close()
# ======================================================================


def data_store():
    '''store the data:
    corpus && weiboVector &&  nutrition && contentEnergy
    '''
    corpus_ptr= file(STORE_DIR + 'corpus', 'w')
    marshal.dump(corpus, corpus_ptr)

    weiboVector_ptr = file(STORE_DIR + 'weiboVector', 'w')
    marshal.dump(weiboVector, weiboVector_ptr)

    nutrition_ptr = file(STORE_DIR + 'nutrition', 'w')
    marshal.dump(nutrition, nutrition_ptr)

    contentEnergy_ptr = open(STORE_DIR +'contentEnergy', 'w')
    marshal.dump(contentEnergy, contentEnergy_ptr)

def data_retrival():
    corpus_ptr= file(STORE_DIR + 'corpus', 'r')
    global corpus
    corpus = marshal.load(corpus_ptr)

    global weiboVector
    weiboVector_ptr = file(STORE_DIR + 'weiboVector', 'r')
    weiboVector = marshal.load(weiboVector_ptr)

    global nutrition
    nutrition_ptr = file(STORE_DIR + 'nutrition', 'r')
    nutrition = marshal.load(nutrition_ptr)

    global contentEnergy
    contentEnergy_ptr = file(STORE_DIR + 'contentEnergy', 'r')
    contentEnergy = marshal.load(contentEnergy_ptr)
    print "len(contentEnergy)", len(contentEnergy)
    print "Successfully retrieve data!"

def time_caculate(r):
    '''
    according to the r and the initTime, calculate the begin time and the end time of r
    --------
    parameter: 
    r: the rth interval,
    --------
    return:
    startTime
    endTime
    '''
    if DAYS == True:
        startTime = initTime + datetime.timedelta(days = r * t)
        endTime = initTime + datetime.timedelta(days = (r+1) * t)
    else:
        startTime = initTime + datetime.timedelta(hours = r * t)
        endTime = initTime + datetime.timedelta(hours = (r+1) * t)
    return startTime, endTime

def store_into_database():
    print 'len(corpus)', len(corpus)
    print 'len(nutrition)', len(nutrition)
    print 'len(energy)', len(energy)
    print 'T', T
    for r in xrange(T):
        startTime, endTime = time_caculate(r)
        for term in corpus[r]:
            encodedTerm = term.encode('utf-8')
            # print encodedTerm, startTime, endTime, nutrition[r][term], energy[r][term]
            cursor.execute("insert into term(value, start_date, end_date, nutrition, energy) values(%s, %s,%s,%s,%s)",[str(encodedTerm), str(startTime), str(endTime), float(nutrition[r][term]), float(energy[r][term])])
        conn.commit()

