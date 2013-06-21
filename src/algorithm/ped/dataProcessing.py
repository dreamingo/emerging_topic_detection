#encoding=utf-8

# from data import *
from sklearn.cluster import AffinityPropagation
import data
import numpy as np
import math

def topic_graph(X, sortedEnergy, r):
    startTime, endTime = data.time_caculate(r)
    print "----------------------"
    af = AffinityPropagation(affinity='precomputed').fit(np.array(X))
    Y = af.labels_
    topics = {}
    for i in xrange(len(Y)):
        if not topics.has_key(Y[i]):
            topics[Y[i]] = set()
        topics[Y[i]].add(i)

    for topic in topics:
        a = tuple(topics[topic])
        if len(a) > 2:
            score = sum([sortedEnergy[i][1] for i in a])/float(len(a))
            print "score:", score
            topicWords = [sortedEnergy[i][0] for i in a]
            t = '/'.join(topicWords).encode('utf-8')
            print t
            weibos,weiboMid = search_weibo(r, topicWords)
            for weibo in weibos[0:3]:
                print weibo[3]
                print '-----------------------------------\n'
            data.cursor.execute("insert into topic(start_date, end_date, topic_content, score, mids) values(%s,%s,%s,%s, %s)",[str(startTime), str(endTime), str(t), float(score), ','.join(weiboMid)])
    data.conn.commit()

def search_weibo(r, topicWords):
    maxScore = 0
    maxMidList = set()
    for weibo in data.weiboVector[r]:
        score = 0
        for word in topicWords:
            if weibo[0].has_key(word):
                score += 1
        if score > maxScore:
            maxScore = score
            maxMidList = set([weibo[2]])
        elif score == maxScore:
            maxMidList.add(weibo[2])
    weibos = []
    for mid in maxMidList:
        data.cursor.execute('select * from weibo_new where mid = "%s"' %(str(mid)))
        weibos.append(data.cursor.fetchone())
    print "maxScore: %s, Len, %s" %(maxScore, len(topicWords))
    return weibos, maxMidList

def correlation_vector(r, sortedEnergy, scalar=50):
    '''关联数组的计算'''
    tempVector = []
    for k in sortedEnergy[0:scalar]:
        k_ = k[0]
        maxValue = 0
        maxItem = k_
        kVector = []
        # r(z,k) means the number of tweets in TWt,k containing keyword k and z
        # Rk means the number of tweets containing keyword k
        # nz means the number of tweets containing keyword z
        # N is the total number of tweet
        for z in sortedEnergy[0:scalar]:
            z_ = z[0]
            if k != z:
                N = len(data.weiboVector[r])
                Rk = len([weibo for weibo in data.weiboVector[r] if weibo[0].has_key(k_)])
                r_z_k = len([weibo for weibo in data.weiboVector[r] if weibo[0].has_key(z_) and weibo[0].has_key(k_)])
                nz = len([weibo for weibo in data.weiboVector[r] if weibo[0].has_key(z_)])
                try:
                    c_k_z = math.log((float(r_z_k)/(Rk - r_z_k))/(float(nz - r_z_k)/(N - nz - Rk + r_z_k)), 2) * math.fabs(float(r_z_k)/Rk - float(nz - r_z_k)/(N - Rk))
                except Exception as e:
                    if Rk == r_z_k:
                        c_k_z = 10
                    else:
                        c_k_z = 0
            else:
                c_k_z = 0
            kVector.append(c_k_z)
            # if c_k_z > maxValue:
            #     maxValue = c_k_z
            #     maxItem = z

        tempVector.append(kVector)
    return tempVector

