import cPickle
import login
import configure
import time

file_ptr = open("../data/new_user", 'r')
users = cPickle.load(file_ptr)
id_users = {}
id_list = set()
leave_id = []

for i in xrange(0, len(users)):
    id_users[users[i]['id']] = i
    id_list.add(users[i]['id'])

for i in users:
    if not i.has_key('friend_list'):
        leave_id.append(i['id'])

client_id = 0
client= login.APILogin(client_id)
count = 1


def add_friend_list_id():
    for user in users:
        friend_list_id = []
        for id in user['friend_list']:
            friend_list_id.append(id_users[id])

        user['friend_list_id'] = friend_list_id

    data_store()

def data_store():
    file_ptr2 = open("../data/new_user", 'w')
    cPickle.dump(users, file_ptr2)
    file_ptr2.close()
    print "Succefully dump! sleep Time"

def get_friend_list():
    print "leave_id:", len(leave_id)
    for i in leave_id:
        try:
            time.sleep(1)
            if(count % 100 == 0):
                data_store()

            ids = client.get.friendships__friends__ids(uid = int(i), count=1000)
            count +=1
            ids = ids['ids']
            is_in = set()
            for k in  ids:
                if k in id_list:
                    is_in.add(k)
            users[id_users[i]]['friend_list'] = is_in
            print "count", count, users[id_users[i]]['name'].encode('utf-8'), len(is_in)

        except:
            leave_id.append(i)
            print "================================="
            print "Exception !!!!!!!!!!!!!!!!!!!!!!!"
            global client
            client_id += 1
            client = login.APILogin((client_id) % configure.APP_COUNT)
            data_store()
            time.sleep(60)

    file_ptr3 = open("../data/leave_id", "w")
    cPickle.dump(leave_id, file_ptr3)
    data_store()

if __name__ == "__main__":
    add_friend_list_id()
