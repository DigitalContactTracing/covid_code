from load_temporal_graph import load_df, build_graphs, get_array_of_contacts
from load_temporal_graph import load_df_socio, build_graphs_socio
import os.path
import os
import pickle


def get_DTU_graph(temporal_gap, n_individuals=None, n_row=None):
    name = 'DTU'
    csv_file = 'Dataset/bt_symmetric.csv'
    graphs = get_graph_from_csv(name, csv_file, temporal_gap, n_individuals, n_row)
    
    return graphs


def temporal_graph_save(graphs, name):
    path = 'Graphs/' + name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
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


def get_graph_from_csv(name, csv_file, temporal_gap, n_individuals=None, n_row=None):
    name += '_temporal_gap_%.0f' % temporal_gap
    
    if os.path.exists('Graphs/' + name + '/'):
        print('Graph already computed: load from memory')
        graphs = temporal_graph_load(name)
    else:
        print('Graph not already computed: build from data')
        df = load_df(csv_file, n_individuals=n_individuals, n_row=n_row)
        graphs = build_graphs(get_array_of_contacts(df, temporal_gap, column_name='# timestamp'), 
                                                    temporal_gap)
        temporal_graph_save(graphs, name)
    return graphs


def get_graph_socio_from_csv(name, csv_file, temporal_gap, extend=None, n_row=None):
    name += '_temporal_gap_%.0f' % temporal_gap
    
    if os.path.exists('Graphs/' + name + '/'):
        print('Graph already computed: load from memory')
        graphs = temporal_graph_load(name)
    else:
        print('Graph not already computed: build from data')
        df = load_df_socio(csv_file, extend, n_row=n_row)
        graphs = build_graphs_socio(get_array_of_contacts(df, temporal_gap, column_name='time'), 
                                                    temporal_gap)
        temporal_graph_save(graphs, name)
    return graphs