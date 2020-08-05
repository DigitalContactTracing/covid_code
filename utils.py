from load_temporal_graph import load_df, build_graphs, get_array_of_contacts
import os.path
import os
import pickle


def get_DTU_graph(temporal_gap, n_individuals=None, n_row=None):
    name = 'DTU_temporal_gap_%.0f' % temporal_gap
    
    if os.path.exists('Graphs/' + name + '/'):
        graphs = temporal_graph_load(name)
    else:
        df = load_df('Dataset/bt_symmetric.csv', n_individuals=n_individuals, n_row=n_row)
        graphs = build_graphs(get_array_of_contacts(df, temporal_gap, column_name='# timestamp'), 
                                                    temporal_gap)
        temporal_graph_save(graphs, name)
    return graphs


def temporal_graph_save(graphs, name):
    path = 'Graphs/' + name + '/'
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path + 'num_snapshots.txt', 'w') as output:
        output.write('%f' % len(graphs))
    for idx, graph in enumerate(graphs):
        with open(path + 'graph_%d.pkl' % idx, 'wb') as output:
            pickle.dump(graph, output, pickle.HIGHEST_PROTOCOL)


def temporal_graph_load(name):        
    path = 'Graphs/' + name + '/'

    with open(path + 'num_snapshots.txt', 'r') as input:
        n_graphs = int(float(input.read()))
    
    graphs = []    
    for idx in range(n_graphs):
        with open(path + 'graph_%d.pkl' % idx, 'rb') as input:
            graph = pickle.load(input)
            graphs.append(graph)
    return graphs

