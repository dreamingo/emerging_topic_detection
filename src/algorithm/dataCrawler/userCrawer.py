#coding=utf-8
import schoolAnalysis
from debug import dprintf
import login
import cPickle
import traceback
from crawler import isSYSU
client = login.APILogin() #API Login
login.browserLogin();     #browserLogin

userList = []   #usd to store the information of the target users;
userIdList = [] #used to record the id of the recorded user
userQueue = []  #as a BFS, used to store the user node



'''Get the common friend between me and Zhongda Din
@return value: will be treated as the first seed users;
'''
def get_my_sysus():
    targetID = 1994626454 # id of Zhongda Din
    commonFriend = client.get.friendships__friends_chain__followers(
            uid = targetID, count = 200)
    return commonFriend

def pre_load_data():
    #load the data from the existing data
    userList_ptr = open("../data/userList", "r")
    userIDList_ptr = open("../data/idList", "r")
    userQueue_ptr = open("../data/queue", "r")

    global userList 
    userList = cPickle.load(userList_ptr)

    global userIdList
    userIdList = cPickle.load(userIDList_ptr)

    global userQueue 
    userQueue = cPickle.load(userQueue_ptr)

    userList_ptr.close()
    userIDList_ptr.close()
    userQueue_ptr.close()

    print "len(userList)",len(userList)
    print "len(userIdList)",len(userIdList)
    print "len(userQueue)",len(userQueue)

    return len(userList)


def data_store():

    print "==============================="
    print "store the data!!!!!"
    userList_ptr = open("../data/userList", "w")
    userIDList_ptr = open("../data/idList", "w")
    userQueue_ptr = open("../data/queue", "w")
    cPickle.dump(userIdList, userIDList_ptr)
    cPickle.dump(userList, userList_ptr)
    cPickle.dump(userQueue, userQueue_ptr)

    userList_ptr.close()
    userIDList_ptr.close()
    userQueue_ptr.close()
    print "len(userList)", len(userList)
    print "len(idList)", len(userIdList)



def userCrawler(useData):

    if not useData:
        seed = get_my_sysus()
        userNum = 0
        for each in seed['users']:
            userNum += 1
            userList.append(each)
            userIdList.append(each['idstr'])
            userQueue.append(each['idstr'])
    else:
        userNum = pre_load_data()

    # BFS
    while (len(userQueue) and userNum <= 5000):
        try:
            topId = userQueue.pop(0)
            # get all the friend of topId user
            cursor = 0
            firstTime = True
            while (cursor or firstTime):
                friends = client.get.friendships__friends(uid = int(topId), count=200,cursor = cursor)
                firstTime = False
                cursor = friends['next_cursor']
                for each in friends['users']:
                    # judge reduplication
                    if each['idstr'] not in userIdList:
                        if isSYSU("http://weibo.com/" + each['idstr']):
                            userNum +=1
                            if userNum%100 == 0:
                                data_store()
                            print each['name'].encode('utf-8'), userNum
                            userList.append(each)
                            userQueue.append(each['idstr'])

                        userIdList.append(each['idstr'])

        except Exception as e:
            print e
            print "Pause end!"
            data_store()
            print traceback.print_exc()

    print "len(userQueue)", len(userQueue)
    print "userNum",userNum 
if __name__== "__main__":
    userCrawler(True)

