import pandas as pd 
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
#import seaborn.apionly as sns
import matplotlib.animation
import random


def remove_individuals(df,n_individuals):
    a = list(df["user_a"].unique())
    b = list(df["user_b"].unique())
    a.extend(b)
    individuals = np.unique(a)
    new_individuals = random.choices(individuals,k=n_individuals)

    df = df.loc[df['user_a'].isin(new_individuals)]
    df = df.loc[df['user_b'].isin(new_individuals)]
    
    return(df)


def load_df(file_name,n_individuals = None,n_row=None,seed=None):
    '''
        given the file name it loads a csv into df
    '''
    
    df = pd.read_csv(file_name)
    df = df.drop(df[(df.user_b == -1)].index)
    df = df.drop(df[(df.user_b == -2)].index)

    if(seed != None):
        random.seed(seed)

    if (n_row != None): 
        df = df.head(n_row)

    if (n_individuals != None):
        remove_individuals(df,n_individuals)
    
    return(df)



def get_array_of_contacts(df,temporal_gap):
    '''
    given a temporal gap it returns an array of dataframes filtered by temporal gap
    '''

    static_contacts = []

    for i in range(int(max(df["# timestamp"].unique()) / temporal_gap)):
        if i == (int(max(df["# timestamp"].unique()) / temporal_gap))-1:
            tmp = df.loc[(df['# timestamp'] >= (i)*temporal_gap)]
        else:
            tmp = df.loc[(df['# timestamp'] >= i*temporal_gap) & (df['# timestamp'] < (i+1)*temporal_gap)]
        static_contacts.append(tmp.copy())

    return(static_contacts)

def get_individuals(df):
    user_A = list(df.user_a.unique())
    user_B = list(df.user_b.unique())
    user_A.extend(user_B)
    nodes_list = np.unique(user_A)

    return(nodes_list) 


def build_graphs(static_contacts,temporal_gap):
    '''
    it returns an array of graphs, in wich each graph represent interactions between nodes.
    Each edge has two attributes rssi and duration, where rssi is the power of the bluethoot signal
    and duration is the cumulative duration of the relationship among peopele.

    If two users keep tolking for a multiple temporal gap, then the rssi signal is averaged!
    '''
    graphs = []
    for contact in static_contacts:

        contact = contact[["user_a","user_b","rssi"]]

        edge_list = []
        for index, row in contact.iterrows():
            edge_list.append(str(row['user_a'])+" "+str(row['user_b'])+" "+str(row["rssi"]))

        G = nx.parse_edgelist(edge_list, nodetype = int, data=(('rssi',float),))
        graphs.append(G)
    
    #### add_cuulative duration

    for e in graphs[0].edges():
        graphs[0].edges()[e]["duration"] = temporal_gap
        
    for i in range(len(graphs)-1):
        g0 = graphs[i]
        g = graphs[i+1]
        for u,v in g.edges():
            if (g0.has_edge(u,v)):
                old_rssi = g0[u][v]["rssi"]
                old_duration = g0[u][v]["duration"]
                g[u][v]["duration"] = old_duration + temporal_gap
                g[u][v]["rssi"] = np.mean([g0[u][v]["rssi"],old_rssi])

            else:
                g[u][v]["duration"] = temporal_gap
        
    return(graphs)


##### socio
def load_df_socio(file_name,extend=True,n_row=None,seed=None):
    
    df = pd.read_csv(file_name,sep=" ")
    df = df[['time', 'a','b']]

    if(seed != None):
        random.seed(seed)

    if (n_row != None): 
        df = df.head(n_row)
        
    # start time = 0
    df.time = df.time - df.time[0]
    if (extend):
        df1 = df.copy()
        df1.time = df.time + max(df.time)+20
        df2 = df1.copy()
        df2.time = df1.time + max(df1.time)+20
        frames = [df,df1,df2]
        df = pd.concat(frames,ignore_index=True)

    return(df)
def get_array_of_contacts_socio(df,temporal_gap):
    '''
    given a temporal gap it returns an array of dataframes filtered by temporal gap
    '''

    static_contacts = []

    for i in range(int(max(df["time"].unique()) / temporal_gap)):
        if i == (int(max(df["time"].unique()) / temporal_gap))-1:
            tmp = df.loc[(df['time'] >= (i)*temporal_gap)]
        else:
            tmp = df.loc[(df['time'] >= i*temporal_gap) & (df['time'] < (i+1)*temporal_gap)]
        static_contacts.append(tmp.copy())

    return(static_contacts)


def build_graphs_socio(static_contacts,temporal_gap):
    '''
    it returns an array of graphs, in wich each graph represent interactions between nodes.
    Each edge has two attributes rssi and duration, where rssi is the power of the bluethoot signal
    and duration is the cumulative duration of the relationship among peopele.

    If two users keep tolking for a multiple temporal gap, then the rssi signal is averaged!
    '''
    graphs = []
    for contact in static_contacts:

        contact = contact[["a","b"]]

        edge_list = []
        for index, row in contact.iterrows():
            edge_list.append(str(row['a'])+" "+str(row['b']))

        G = nx.parse_edgelist(edge_list)
        graphs.append(G)
    
    #### add_cuulative duration

    for e in graphs[0].edges():
        graphs[0].edges()[e]["duration"] = temporal_gap
        
    for i in range(len(graphs)-1):
        g0 = graphs[i]
        g = graphs[i+1]
        for u,v in g.edges():
            if (g0.has_edge(u,v)):
                old_duration = g0[u][v]["duration"]
                g[u][v]["duration"] = old_duration + temporal_gap

            else:
                g[u][v]["duration"] = temporal_gap
        
    return(graphs)










def compute_comulative(graphs):
    cumulative_graphs = [nx.compose(graphs[0],graphs[1])]
    c = 1
    for i in graphs[1:]:
        union = nx.compose(cumulative_graphs[-1],i)
        cumulative_graphs.append(union)
    return(cumulative_graphs)

def show_animation(graphs,save=None):
    cumulative_graphs = compute_comulative(graphs)
    pos = nx.spring_layout(cumulative_graphs[-1])
    fig, ax = plt.subplots(figsize=(5,5))

    def update(num):
        ax.clear()
        connected_nodes = set(list(cumulative_graphs[num].nodes())).difference(list(nx.isolates(cumulative_graphs[num])))
        nx.draw(nx.subgraph(cumulative_graphs[num],connected_nodes),pos=pos,node_size=20,alpha=0.1)
        new_conn_nodes = set(list(graphs[num].nodes)).difference(list(nx.isolates(graphs[num])))
        nx.draw(nx.subgraph(graphs[num],new_conn_nodes),pos=pos,node_size=20)

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=len(graphs), interval=500, repeat=True)

    if not(save == None):

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=1800)
        ani.save('im.mp4', writer=writer)
    else:
        return(ani)
