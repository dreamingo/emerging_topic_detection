import networkx as nx
import cPickle
import matplotlib.pyplot as plt

def generate_g():
    file_ptr = open('../data/new_user', 'r')
    users = cPickle.load(file_ptr)
    lines = []
    for i in xrange(0, len(users)):
        for index in users[i]['friend_list_id']:
            lines.append((i, index))
    G = nx.DiGraph()
    G.add_edges_from(lines)

    print "num of nodes", len(G.nodes())
    print "Num of edges", len(G.edges())
    max_index = 0
    max_num = 0
    for i in G.nodes():
        if G.in_degree(i) > max_num:
            max_num = G.in_degree(i)
            max_index = i
    # max_node = max([G.in_degree(k) for k in G.nodes()])
    print "max in_degree", max_num
    print users[max_index]['name'].encode('utf-8')
    nx.draw(G,with_labels = False, pos = nx.shell_layout(G), node_size = 30)
    # plt.savefig('Graph.png')
    plt.show()

def check_dead_end():
    file_ptr = open('../data/new_user', 'r')
    users = cPickle.load(file_ptr)
    for user in users:
        if len(user['friend_list_id']) == 1:
            print user['name'].encode('utf-8')

# generate_g()
check_dead_end()
