#encoding=utf-8
import cPickle
import numpy as np

# Data initilization
# ==================================
file_ptr = open("../data/backup/new_user", "r")
users = cPickle.load(file_ptr)
id_list = []
_id_list = []
for user in users:
    id_list.append(set(user['friend_list_id']))
    _id_list.append(set(user['friend_list_id']))

# =========================================

def deal_with_dead_end():
    '''
    dead_end, 没有指向别人的节点'
    dead_end的存在会使matrix的某i些列变成全0, 导致迭代的失败(矩阵论的知识)
    因此,需要迭代消除dead_end(因为dead_end消除后会产生新的dead_end, 因此需要迭代消除)
    消除dead_end后, 再反向推出dead_end的权值.

    @retrun parameter:
        dead_end_dict:{dead_end_index: [the point who points to the dead_end]} 
        time_line_dead_end [],  used to record the order of the elimination of the dead end
    '''
    dead_end_dict = {}
    time_line_dead_end = []
    dead_end = True
    while dead_end:
        dead_end = False
        dead_end_list = set()
        for i in xrange(0, len(id_list)):
            if not dead_end_dict.has_key(i):
                if len(id_list[i]) == 0:
                    dead_end = True
                    dead_end_list.add(i)
                    dead_end_dict[i] = []
                    time_line_dead_end.append(i)
        for end in dead_end_list:
            for row_i in xrange(0, len(id_list)):
                if end in id_list[row_i]:
                    id_list[row_i].remove(end)
                    dead_end_dict[end].append(row_i)
    return dead_end_dict, time_line_dead_end

def build_matrix():
    '''
    if j->i  Mij = 1/|j|
    else Mij = 0
    '''
    N = 7999
    li = []
    for row_i in xrange(0, len(id_list)):
        if len(id_list[row_i]) == 0:
            for i in xrange(0, N):
                li.append(1./N)
        else:
            for i in xrange(0, N):
                if i in id_list[row_i]:
                    li.append(1./len(id_list[row_i]))
                else:
                    li.append(0)
    matrix = np.array(li, dtype = float).reshape(N,N)
    matrix = matrix.transpose()
    return matrix

def pageRank(matrix,dead_end_dict, time_line_dead_end):
    N = 7999
    b = 0.15 #probability of the teleport 
    r = np.array([1.0/N] * N, dtype = float).reshape(N,1)
    e = np.array([1.0] * N).reshape(N,1)
    for i in xrange(0, 20):
        r = (1-b)*np.dot(matrix, r) + e*b/N 
    for i in xrange(len(time_line_dead_end)-1, -1, -1):
        for j in dead_end_dict[time_line_dead_end[i]]:
            r[time_line_dead_end[i]] += r[j]*(1./len(_id_list[j]))
    return r

if __name__ == "__main__":
    dead_end_dict, time_line_dead_end = deal_with_dead_end()
    matrix = build_matrix()
    r = pageRank(matrix, dead_end_dict, time_line_dead_end)
    # for i in xrange(0, len(r)):
    #     users[i]['authority'] = r[i]
    file_users = open('../data/backup/new_user', 'w')
    cPickle.dump(users, file_users)
    # print r.max()
    # index = np.where(r==r.max())
    # print users[index[0]]['name'].encode('utf-8')
    r_dict = {i:r[i] for i in xrange(0, len(r))}
    from operator import itemgetter
    my_r = sorted(r_dict.iteritems(), key=itemgetter(1), reverse=True)
    for i in my_r[0:100]:
        print users[i[0]]['name'].encode('utf-8'), i[1]



