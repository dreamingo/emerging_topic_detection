import datetime
import data

def train(dataStore):
    import contentExtraction
    for r_ in xrange(0, data.T):
        print "======================"
        weibos = contentExtraction.get_weibo(r_)
        contentExtraction.weibo_vetorization(weibos)
        contentExtraction.content_nutrition(r_)

    for r_ in xrange(0, data.T):
        print "calculatiing the energy of the interval %s ...." %(str(r_))
        contentExtraction.content_energy(r_)
    data.store_into_database()

    if dataStore:
        data.data_store()

def test(retrive_data):
    import dataProcessing
    if retrive_data:
        data.data_retrival()

    startTime = 2
    endTime = data.T

    for r in xrange(startTime, endTime):
        preTime, nextTime = data.time_caculate(r)
        print "\n\n\n====================================================="
        print "between %s and %s," %(str(preTime), str(nextTime))
        vector = dataProcessing.correlation_vector(r, data.contentEnergy[r])
        dataProcessing.topic_graph(vector, data.contentEnergy[r], r)

if __name__ == "__main__":
    DEBUG = False
    data.T = 65
    data.t = 1
    data.DAYS = True
    data.initTime = datetime.datetime(2013,03,27,0,0,0)
    train(dataStore = DEBUG)
    test(retrive_data = DEBUG)
    
