#encoding=utf-8
import chardet
import MySQLdb
from matplotlib import pylab as plt
import cPickle
import numpy as np
import datetime
import os
homedir = os.getcwd()
imgdir = os.path.join(homedir, 'static/img/')

conn = MySQLdb.connect(host='localhost', user='root',passwd='1', db = 'ped_new', charset='utf8')
cursor = conn.cursor()


def weibo_number_analysis():
    initTime = datetime.datetime(2013, 04,01)
    timeinfo = []
    count = []

    for r in xrange(0, 31):
        preTime = initTime + datetime.timedelta(days = r)
        nextTime = initTime + datetime.timedelta(days = r+1)
        c = cursor.execute('select * from weibo_new where publish_time > "%s" and publish_time < "%s"' %(str(preTime), str(nextTime)))
        print "Between %s and %s there are %s weibos" %(preTime, nextTime, c)
        timeinfo.append(str(datetime.date.isoformat(preTime)))
        count.append(c)

    plt.xticks(range(len(timeinfo)), timeinfo, size='small', rotation='vertical')
    plt.ylabel('Number of Tweet')
    plt.xlabel('date')
    # plt.hist(count, 50, normed=1, facecolor='g', alpha=0.75)
    # plt.axis([[0, 30, 5000, 20000]])
    plt.plot(np.arange(0, 31), count, 'bo', np.arange(0, 31),count, 'k')
    plt.show()

def read_data(term):
    count = cursor.execute('select * from term where value = "%s" order by start_date' %(term))
    print 'count', count
    allData = [d for d in cursor.fetchall()]
    print "Successfully read term!"
    return allData
    # file_ptr = open('tmp_data/analysis/word', 'w')
    # cPickle.dump(allData, file_ptr)

def nutrition_energy_analysis(term, dateLenght = 60, startDate = datetime.datetime(2013,04,01)):
    # file_ptr = open('tmp_data/analysis/nutrion', 'r')
    # allData = cPickle.load(file_ptr)
    allData = read_data(term)
    if len(allData) == 0:
        return False
    date = [startDate + datetime.timedelta(r) for r in xrange(dateLenght)]
    dateTicks = [str(datetime.date.isoformat(t)) for t in date]

    nutrition = []
    energy = []
    for d in date:
        has = False
        for data in allData:
            if str(data[1]) == str(d):
                has = True
                nutrition.append(data[3])
                energy.append(data[4])
                break
        if not has:
            nutrition.append(0)
            energy.append(0)

    print len(energy)
    print len(nutrition)
    # plt.axis([0, len(allData)-30, 0., 0.5])
    plt.figure(1)
    plt.xticks(range(len(nutrition)), dateTicks, size='small', rotation='vertical')
    plt.ylim(0,300)
    plt.ylabel('Nutrition')
    plt.xlabel('date')
    x = np.arange(0, dateLenght,1)
    plt.plot(x, nutrition,'bo', x, nutrition, 'k')
    plt.savefig(imgdir + 'nutrition.png')
    plt.clf()
    # plt.show()

    plt.figure(2)
    plt.xticks(range(len(energy)), dateTicks, size='small', rotation='vertical')
    plt.ylabel('Energy')
    plt.ylim(-20000,60000)
    plt.xlabel('date')
    x = np.arange(0, dateLenght,1)
    plt.plot(x, energy,'bo', x, energy, 'k')
    plt.savefig(imgdir + 'energy.png')
    plt.clf()
    # plt.show()
    # raw_input()
    return True

def pageRank_analysis():
    # data = open('authorityRanking', 'r').readlines()
    users = cPickle.load(open('../data/backup/new_user','r'))
    data = {user['name'].encode('utf-8') : user['authority'] for user in users}

    from operator import itemgetter
    data = sorted(data.iteritems(), key=itemgetter(1), reverse = True)
    filePtr = open('userRanking.html', 'w')
    rank = 1
    for d in data:
        filePtr.write('<tr>\n')
        filePtr.write('<td>%s</td>\n' %(str(rank)))
        rank += 1
        for _d in d:
            filePtr.write('<td>%s</td>\n' %(_d))
        filePtr.write('</tr>\n')

if __name__ == "__main__":

    nutrition_energy_analysis('同学')
    # pageRank_analysis()
