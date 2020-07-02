import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import csv
import os
from system_definition import onset_time, beta_data



import json
import os

def store_results(res,PARAMETERS,filter_rssi,filter_duration,eps_I):
    
    path = PARAMETERS["store"]["path_to_store"]
    #store the simulations parameters in JSON file
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+'PARAMETERS.json', 'w') as outfile:
        json.dump(PARAMETERS, outfile, indent=4)
        
    name = "epsI"+str(eps_I)+"_filterRSSI"+str(filter_rssi)+"_filterDuration"+str(filter_duration)
    np.save(path+"eT_"+name+".npy",res[0])
    np.save(path+"sym_"+name+".npy",res[1])
    np.save(path+"iso_"+name+".npy",res[2])
    np.save(path+"act_inf_"+name+".npy",res[3])
    np.save(path+"q_t_"+name+".npy",res[4])
    np.save(path+"q_t_i_"+name+".npy",res[5])
    np.save(path+"Q_nb_"+name+".npy",res[6])
    np.save(path+"Qi_nb_"+name+".npy",res[7])
    np.save(path+"I_"+name+".npy",[res[8]])
    
    print("Simulation saved in ", path)
    
    
# load the results
def load_results(path,file,eps_I,filter_rssi,filter_duration):

    name = "_epsI"+str(eps_I)+"_filterRSSI"+str(filter_rssi)+"_filterDuration"+str(filter_duration)
    loaded_file = np.load(path+file+name+".npy",allow_pickle=True)
    
    return(loaded_file)




def inizialize_contacts(graphs):
    nodes = []
    for g in graphs:
        for n in list(g.nodes()):
            if n not in nodes:
                nodes.append(n)

    contacts = dict()
    for i in nodes:
        contacts[i] = []
    return contacts


def policy(graph, node, filter_rssi, filter_duration):
    if (node in graph):
        neig = graph.neighbors(node)
    else:
        neig = []
    res = []
    for n in neig:
        rssi = graph[node][n]["rssi"]
        duration = graph[node][n]["duration"]

        if (rssi > filter_rssi and duration > filter_duration):
            res.append(n)
    return (res)


def inizialize_infected_time0(Y_i_nodes,I,infected):
    for i in Y_i_nodes:
        tau = np.random.uniform(0,10)  # fra 0 e 10 giorni
        I[i] = {'tau': tau, 'tau_p': None, 'to': onset_time(),'inf': [],'e_inf': [],'ss_inf': [],'ss_p':None,'e_p':None}
        infected.append(i)

    return(Y_i_nodes,I,infected)



def update_contacts(contacts,graph,filter_rssi,filter_duration,memory_contacts):
    for node in list(contacts.keys()):
        res = policy(graph, node, filter_rssi, filter_duration)
        if len(contacts[node]) == memory_contacts:
            contacts[node] = contacts[node][1:]
            contacts[node].append(res)
        else:
            contacts[node].append(res)
    return(contacts)   

def update_quarantened(contacts, quarantined,infected, current_time,max_time_quar):
    for node in list(contacts.keys()):
        if node in quarantined and current_time - quarantined[node]['in_time'] >= max_time_quar:
            quarantined.pop(node)
            if node in I:
                infected.append(node)

    return (quarantined,infected)


def does_not_have_symptoms_or_not_caught(graph,node,I,quarantined,current_time,infected,new_infected):
    if node in graph:
        neigh = list(graph.neighbors(node))
    else:
        neigh = []

    for m in neigh:
        if m not in I and m not in quarantined:
            ss = graph[node][m]["rssi"]  # signal strength
            e = graph[node][m]["duration"]  # exposure (seconds)

            pp = beta_data(I[node]['tau'], ss, e)  # probability of contagion node --> m
            rr = np.random.uniform(0, 1)
            if rr < pp:  # avviene il contagio di m
                to = onset_time()
                I[m] = {'tau': 0, 'tau_p': I[node]['tau'], 'to': current_time + to, 'inf': [],'e_inf': [],'ss_inf': [],'ss_p':ss,'e_p':e}
                I[node]["inf"].append(m)
                I[node]["e_inf"].append(e)
                I[node]["ss_inf"].append(ss)

                infected.append(m)
                new_infected.append(m)

    return (I,infected,new_infected)

def have_symptoms(isolated,quarantined,current_time,infected,NC_nodes,contacts,node,I,eTt):
    if node in isolated:
        print('error: isolated', node, 'time', current_time)
    if node in quarantined:
        print('error: quar')
    if node not in infected:
        print('error: not inf')
    isolated.append(node)
    infected.remove(node)

    if node not in NC_nodes:
        
        C = [item for sublist in contacts[node] for item in sublist]
        C = np.unique(C)

        for m in C:  # unique
            if m not in quarantined and m not in isolated and m not in NC_nodes:
                if m in infected:  
                    quarantined[m] = {'in_time': current_time, 'infected': 'yes'}
                    infected.remove(m)  # m e' in quarantena quindi anche se era infetto non e' piu' attivo

                else:
                    quarantined[m] = {'in_time': current_time, 'infected': 'no'}


        if I[node]["inf"] != []:
            eTn = 0
            for inf in I[node]["inf"]:  # conto quanti ne ho lasciati fuori
                if inf not in C:
                    # print("rimasto fuori")
                    eTn += 1
            eTn /= len(I[node]["inf"])
            eTt.append(eTn)

    return(isolated,infected,quarantined,eTt)

def simulate(graphs, Y_i_nodes, NC_nodes, eps_I, temporal_gap, filter_rssi, filter_duration, memory_contacts, max_time_quar, beta_data=beta_data, onset_time=onset_time):
    I = dict()
    infected = []  # active_infected
    isolated = []
    quarantined = dict()
    symptomatic = []
    eT = []
    memory_contacts = int(memory_contacts * 24 * 3600 / temporal_gap) 
    max_time_quar = max_time_quar * 24 * 3600
    contacts = inizialize_contacts(graphs)
    sym_t = []
    iso_t = []
    act_inf_t = []
    q_t = []
    q_t_i = []
    Q_list = []
    Qi_list = []


    # inizialize I and infected for the input persons infected
    Y_i_nodes,I,infected = inizialize_infected_time0(Y_i_nodes,I,infected)


    current_time = 0
    for graph in graphs:

        new_infected = []
        eTt = []

        # update tracing contacts
        contacts = update_contacts(contacts,graph,filter_rssi,filter_duration,memory_contacts)

        # remove from the quarantain people that does not present symptoms
        quarantined,infected = update_quarantened(contacts, quarantined,infected, current_time,max_time_quar)




        for node in list(I.keys()).copy():
            current_to = I[node]["to"]
            I[node]["tau"] = I[node]["tau"] + temporal_gap / (3600 * 24) #update tau
            current_tau = I[node]['tau']

            if current_to <= current_time:  # diventa sintomatico
                if node not in symptomatic:
                    symptomatic.append(node)

            if node in infected:
                r = np.random.uniform(0, 1)

                if current_to > current_time or r > eps_I:  # non ha sintomi o non lo becco?
                    I,infected,new_infected = does_not_have_symptoms_or_not_caught(graph,
                                                                                    node,
                                                                                    I,
                                                                                    quarantined,
                                                                                    current_time,
                                                                                    infected,
                                                                                    new_infected)

                elif current_to <= current_time and r <= eps_I:  # ha sintomi e lo becco 
                    isolated,infected,quarantined,eTt = have_symptoms(isolated,
                                                                        quarantined,
                                                                        current_time,
                                                                        infected,
                                                                        NC_nodes,
                                                                        contacts,
                                                                        node,
                                                                        I,
                                                                        eTt)



                    


        # se quelli in quarantena presentano sintomi
        for q in quarantined.copy():
            if q in I:
                current_to = I[q]["to"]

                if current_to < current_time:  # presentano sintomi
                    assert q not in isolated  #### sempre true
                    isolated.append(q)
                    quarantined.pop(q)  # rimuovo q dalla quarantena

                    C = []
                    if q not in NC_nodes:
                        for contacts_list in contacts[q]:  # i contatti che ha avuto q negli ultimi 10 giorni (solo quelli prima della quarantena)
                            for contact in contacts_list:
                                if contact not in C:
                                    C.append(contact)
                        for m in C:  # unique

                            if m not in quarantined and m not in isolated and m not in NC_nodes:
                                if m in infected: 
                                    quarantined[m] = {'in_time': current_time, 'infected': 'yes'}
                                    infected.remove(m)  # m e' in quarantena quindi anche se era infetto non e' piu' attivo
                                else:
                                    quarantined[m] = {'in_time': current_time, 'infected': 'no'}


                    if I[q]["inf"] != []:
                        eTn = 0
                        for inf in I[q]["inf"]:  # conto quanti ne ho lasciati fuori
                            if inf not in C:
                                eTn += 1
                        eTn /= len(I[q]["inf"])
                        eTt.append(eTn)


        if eTt != []:
            eT.append(np.mean(eTt))

        sym_t.append(len(symptomatic))
        iso_t.append(len(isolated))
        act_inf_t.append(len(infected))
        q_t.append(len(quarantined))
        Q_list.extend(quarantined.keys())
        q_t_ingiustamente = 0
        for node in quarantined:
            if quarantined[node]['infected'] == 'no':
                q_t_ingiustamente += 1
                Qi_list.append(node)
        q_t_i.append(q_t_ingiustamente)

        quar_g_len = len(quarantined) - q_t_ingiustamente  # quanti giustamente in quarantena

        current_time = current_time + temporal_gap

    Q_nb = len(np.unique(Q_list))
    Qi_nb = len(np.unique(Qi_list))


    return (eT, sym_t, iso_t, act_inf_t, q_t, q_t_i, Q_nb, Qi_nb, I)






