#encoding=utf-8
import jieba
import datetime
import marshal
import math
import numpy as np
import re
import json
from operator import itemgetter
import data
from matplotlib import pylab as plt

def get_weibo(r):
    '''parameter: interval <It, It+r>
    '''
    preTime, nextTime = data.time_caculate(r)
    count = data.cursor.execute('select * from weibo_new where publish_time > "%s" and publish_time < "%s"' %(str(preTime), str(nextTime)))
    print "between %s and %s, there is %s weibos" %(str(preTime), str(nextTime), str(count))
    # return count, preTime
    return data.cursor.fetchall()

def weibo_vetorization(weibos):
    '''
    微薄向量化
    a.对一条微薄进行分词, 返回得到一个list;
    b.根据list, 构建dict{term: termFrequency};
    所有的微薄的存储:[ [{dict}, userid],[{dict}, userid].... ]
    '''
    vectors = []
    interval_corpus = set()
    for weibo in weibos:
        splitWords = list(jieba.cut(weibo[3]))
        wordFrequency = {}
        allCount = 0
        for word in splitWords:
            #get rid of the term with single word and stopword
            if len(word) >= 2 and word not in data.stopWord:                 
                interval_corpus.add(word)
                allCount += 1
                if wordFrequency.has_key(word):
                    wordFrequency[word] += 1
                else:
                    wordFrequency[word] = 1

        maxFre = 0
        for i in wordFrequency.itervalues():
            if i > maxFre:
                maxFre = i
        # caculate the weight of each term in each tweet
        for item in wordFrequency:
            wordFrequency[item] = [0.5 + 0.5 * (float(wordFrequency[item]) / maxFre), float(wordFrequency[item])/allCount]

        vectors.append([wordFrequency, weibo[1], weibo[0], allCount])

    data.weiboVector.append(vectors)
    data.corpus.append(interval_corpus)

def content_nutrition(r):
    '''
    词语营养学
    a. 对于每个term, 找出在interval t中哪些微博Tw 含有这一个term:
    计算 term_nutrition(i) = sum(termWeight(i, j)*authority[user(weibo[j])])
    '''
    interval_nutrition = {}
    for term in data.corpus[r]:
        termNutr = 0.
        for weibo in data.weiboVector[r]:
            if weibo[0].has_key(term):
                termNutr += weibo[0][term][0] * data.authority[weibo[1]]

        interval_nutrition[term] = 1000 * termNutr
    data.nutrition.append(interval_nutrition)
    print "Content_nutrition %s done" %(str(r))

def content_energy(r):
    '''
    算出每个词语的content energy
    term_energy(i) = sum(nutrition[i]** - nutri_i[s][i]**2)*(1.(r - i)*(r - i))
    '''
    intervalEnergy = {}
    begin = r - 10
    if begin < 0:
        begin = 0

    for term in data.nutrition[r]:
        intervalEnergy[term] = 0
        for i in xrange(begin, r):
            if not data.nutrition[i].has_key(term):
                nutr_i = 0
            else:
                nutr_i = data.nutrition[i][term]
            intervalEnergy[term] += (data.nutrition[r][term]**2 - nutr_i**2)*(1./(r-i))

    data.energy.append(intervalEnergy)
    from operator import itemgetter
    temp = sorted(intervalEnergy.iteritems(), key=itemgetter(1), reverse=True)
    data.contentEnergy.append(temp)

def test():
    data.initTime = datetime.datetime(2013,04,01,02,0,0)
    data.t = 1
    data.DAYS = True
    c = []
    t = []
    for r in xrange(0, 40):
        count, time = get_weibo(r)
        c.append(count)
        t.append(time)
    plt.xticks(range(len(c)), t, size='small', rotation='vertical')
    plt.ylabel('Number Of Weibo')
    plt.xlabel('date')
    x = np.arange(0, len(c), 1)
    plt.plot(x, c,'bo', x, c, 'k')
    plt.show()

if __name__ == "__main__":
    test()

