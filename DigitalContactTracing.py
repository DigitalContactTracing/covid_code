import numpy as np
import load_temporal_graph as LTG
from system_definition import *

import json
import csv
import os


def store_real_time(res,PARAMETERS,filter_rssi,filter_duration,eps_I):


    def save_on_csv(filename,variable_list,writing_operation):
        with open(filename, writing_operation) as csvfile:
            writer = csv.writer(csvfile)
            try:
                [writer.writerow(s) for s in variable_list]
            except:
                writer.writerow(variable_list)
        #print("saved ", filename)


    path = PARAMETERS["store"]["path_to_store"]
    #store the simulations parameters in JSON file
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+'PARAMETERS.json', 'w') as outfile:
        json.dump(PARAMETERS, outfile, indent=4)


    name = "epsI"+str(eps_I)+"_filterRSSI"+str(filter_rssi)+"_filterDuration"+str(filter_duration)
    results = np.array(res)



    writing_operation = "a+"
    save_on_csv(path+"eT_"+name+".csv",results[0],writing_operation)
    save_on_csv(path+"sym_"+name+".csv",results[1],writing_operation)
    save_on_csv(path+"iso_"+name+".csv",results[2],writing_operation)
    save_on_csv(path+"act_inf_"+name+".csv",results[3],writing_operation)
    save_on_csv(path+"q_t_"+name+".csv",results[4],writing_operation)
    save_on_csv(path+"q_t_i_"+name+".csv",results[5],writing_operation)
    save_on_csv(path+"Q_nb_"+name+".csv",results[6],writing_operation)
    save_on_csv(path+"Qi_nb_"+name+".csv",results[7],writing_operation)
    name_I = path+"I_"+name+".npy"
    if os.path.exists(name_I):
        old = list(np.load(name_I,allow_pickle=True))
        old.append(results[8])
        np.save(name_I,old)
    else:
        np.save(name_I,results[8])
    
# load the results
def load_results(path,file,eps_I,filter_rssi,filter_duration):
    name = path+file+"_epsI"+str(eps_I)+"_filterRSSI"+str(filter_rssi)+"_filterDuration"+str(filter_duration)+".csv"
    loaded_file = []
    if (file == "I"):
        name = path+file+"_epsI"+str(eps_I)+"_filterRSSI"+str(filter_rssi)+"_filterDuration"+str(filter_duration)+".npy"
        loaded_file = list(np.load(name,allow_pickle=True))
    else:
        with open(name, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if file =="eT":
                    float_row = [float(i) for i in row]
                    loaded_file.append(float_row)
                else:
                    int_row = [int(i) for i in row]
                    loaded_file.append(int_row)

    return(loaded_file)
'''

def store_results(res,PARAMETERS,filter_rssi,filter_duration,eps_I):
    
    path = PARAMETERS["store"]["path_to_store"]
    #store the simulations parameters in JSON file
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+'PARAMETERS.json', 'w') as outfile:
        json.dump(PARAMETERS, outfile, indent=4)
        
    name = "epsI"+str(eps_I)+"_filterRSSI"+str(filter_rssi)+"_filterDuration"+str(filter_duration)
    results = np.array(res)
    
    
    np.save(path+"eT_"+name+".npy",results[:,0])
    np.save(path+"sym_"+name+".npy",results[:,1])
    np.save(path+"iso_"+name+".npy",results[:,2])
    np.save(path+"act_inf_"+name+".npy",results[:,3])
    np.save(path+"q_t_"+name+".npy",results[:,4])
    np.save(path+"q_t_i_"+name+".npy",results[:,5])
    np.save(path+"Q_nb_"+name+".npy",results[:,6])
    np.save(path+"Qi_nb_"+name+".npy",results[:,7])
    np.save(path+"I_"+name+".npy",[results[:,8]])
    
    print("Simulation saved in ", path)
    

    
    
# load the results
def load_results(path,file,eps_I,filter_rssi,filter_duration):

    name = "_epsI"+str(eps_I)+"_filterRSSI"+str(filter_rssi)+"_filterDuration"+str(filter_duration)
    loaded_file = np.load(path+file+name+".npy",allow_pickle=True)
    
    return(loaded_file)
'''


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



def policy(graph, node, filter_rssi, filter_duration,SOCIOPATTERN):
    if (node in graph):
        neig = graph.neighbors(node)
    else:
        neig = []
    res = []
    for n in neig:
        if not(SOCIOPATTERN):
            rssi = graph[node][n]["rssi"]
            duration = graph[node][n]["duration"]
            if (rssi > filter_rssi and duration > filter_duration):
                res.append(n)
        else:
            duration = graph[node][n]["duration"]
            if (duration > filter_duration):
                res.append(n)

    return (res)


def inizialize_infected_time0(self):
    for i in self.Y_i_nodes:
        tau = np.random.uniform(0,10)  # fra 0 e 10 giorni
        self.I[i] = {'tau': tau, 'tau_p': None, 'to': onset_time(symptomatics=self.sympt, testing=self.test),'inf': [],'e_inf': [],'ss_inf': [],'ss_p':None,'e_p':None}
        self.infected.append(i)


class DigitalContactTracing:

    def __init__(self, graphs,PARAMETERS,eps_I,filter_rssi,filter_duration,SOCIOPATTERN = False):

        self.I = dict()
        self.infected = []  # active_infected
        self.isolated = []
        self.quarantined = dict()
        self.symptomatic = []
        self.eT = []
        self.temporal_gap = PARAMETERS["temporal_gap"]
        self.memory_contacts = int(PARAMETERS["memory_contacts"] * 24 * 3600 / self.temporal_gap) 
        self.max_time_quar = PARAMETERS["max_time_quar"] * 24 * 3600
        self.contacts = inizialize_contacts(graphs)
        self.sym_t = []
        self.iso_t = []
        self.act_inf_t = []
        self.q_t = []
        self.q_t_i = []
        self.Q_list = []
        self.Qi_list = []
        self.sympt = PARAMETERS["symptomatics"]
        self.test = PARAMETERS["testing"]
        self.eps_I = eps_I
        self.filter_rssi = filter_rssi
        self.filter_duration = filter_duration
        self.graphs = graphs
        self.beta_t = PARAMETERS["beta_t"]
        self.SOCIOPATTERN = SOCIOPATTERN

        
        nodes_list = LTG.get_individuals_from_graphs(graphs)
        NC = round(PARAMETERS["nc"]*len(nodes_list)) # nb of non-compliant

        # get infected at time 0
        individuals_0 = list(graphs[0].nodes())
        np.random.shuffle(individuals_0)
        self.Y_i_nodes = individuals_0[0:PARAMETERS["Y_i"]]

        # get people that are using the app
        np.random.shuffle(nodes_list)
        self.NC_nodes = nodes_list[0:NC]

        inizialize_infected_time0(self)


    def simulate(self):
        current_time = 0
        for graph in self.graphs:

            new_infected = []
            self.eTt = []

            # update tracing contacts
            self.update_contacts(graph)

            # remove from the quarantain people that does not present symptoms
            self.update_quarantened(current_time)


            for node in list(self.I.keys()).copy():
                current_to = self.I[node]["to"]
                self.I[node]["tau"] = self.I[node]["tau"] + self.temporal_gap / (3600 * 24) #update tau
                current_tau = self.I[node]['tau']

                if current_to <= current_time:  # diventa sintomatico
                    if node not in self.symptomatic:
                        self.symptomatic.append(node)

                if node in self.infected:

                    r = np.random.uniform(0, 1)

                    if current_to > current_time or r > self.eps_I:  # non ha sintomi o non lo becco?
                        self.does_not_have_symptoms_or_not_caught(graph,node,new_infected,current_time)
                    
                    elif current_to <= current_time and r <= self.eps_I:  # ha sintomi e lo becco 
                        self.have_symptoms(current_time,node,in_qurantain=False)



                    


            # se quelli in quarantena presentano sintomi
            for node in self.quarantined.copy():
                if node in self.I:
                    current_to = self.I[node]["to"]

                    if current_to < current_time:  # presentano sintomi
                        self.have_symptoms(current_time,node,in_qurantain=True)




            if self.eTt != []:
                self.eT.append(np.mean(self.eTt))

            self.sym_t.append(len(self.symptomatic))
            self.iso_t.append(len(self.isolated))
            self.act_inf_t.append(len(self.infected))
            self.q_t.append(len(self.quarantined))
            self.Q_list.extend(self.quarantined.keys())
            q_t_ingiustamente = 0
            for node in self.quarantined:
                if self.quarantined[node]['infected'] == 'no':
                    q_t_ingiustamente += 1
                    self.Qi_list.append(node)
            self.q_t_i.append(q_t_ingiustamente)

            quar_g_len = len(self.quarantined) - q_t_ingiustamente  # quanti giustamente in quarantena

            current_time = current_time + self.temporal_gap

        self.Q_nb = len(np.unique(self.Q_list))
        self.Qi_nb = len(np.unique(self.Qi_list))


        return ([self.eT, self.sym_t, self.iso_t, self.act_inf_t, self.q_t, self.q_t_i, [self.Q_nb], [self.Qi_nb], [self.I]])






    def have_symptoms(self,current_time,node,in_qurantain):
        
        assert node not in self.isolated # error: isolated
        
        if not(in_qurantain): # if person in quarantain
            assert node not in self.quarantined # error: quar
            assert node in self.infected # error: not inf

            self.isolated.append(node)
            self.infected.remove(node) 
        else: # if person non in qurantain
            self.isolated.append(node)
            self.quarantined.pop(node) 

        C = []

        if node not in self.NC_nodes:
            
            C = [item for sublist in self.contacts[node] for item in sublist]
            C = np.unique(C)

            for m in C:  # unique
                if m not in self.quarantined and m not in self.isolated and m not in self.NC_nodes:
                    if m in self.infected:  
                        self.quarantined[m] = {'in_time': current_time, 'infected': 'yes'}
                        self.infected.remove(m)  # m e' in quarantena quindi anche se era infetto non e' piu' attivo

                    else:
                        self.quarantined[m] = {'in_time': current_time, 'infected': 'no'}


        if self.I[node]["inf"] != []:
            eTn = 0
            for inf in self.I[node]["inf"]:  # conto quanti ne ho lasciati fuori
                if inf not in C:
                    # print("rimasto fuori")
                    eTn += 1
            eTn /= len(self.I[node]["inf"])
            self.eTt.append(eTn)




    def does_not_have_symptoms_or_not_caught(self,graph,node,new_infected,current_time):
        if node in graph:
            neigh = list(graph.neighbors(node))
        else:
            neigh = []

        for m in neigh:
            if m not in self.I and m not in self.quarantined:
                if not(self.SOCIOPATTERN):
                    ss = graph[node][m]["rssi"]  # signal strength
                else:
                    ss = 0
                e = graph[node][m]["duration"]  # exposure (seconds)

                pp = beta_data(self.I[node]['tau'], ss, e,self.beta_t)  # probability of contagion node --> m
                rr = np.random.uniform(0, 1)
                if rr < pp:  # avviene il contagio di m
                    to = onset_time(symptomatics=self.sympt, testing=self.test)
                    self.I[m] = {'tau': 0, 'tau_p': self.I[node]['tau'], 'to': current_time + to, 'inf': [],'e_inf': [],'ss_inf': [],'ss_p':ss,'e_p':e}
                    self.I[node]["inf"].append(m)
                    self.I[node]["e_inf"].append(e)
                    self.I[node]["ss_inf"].append(ss)

                    self.infected.append(m)
                    new_infected.append(m)



    def update_contacts(self,graph):
        for node in list(self.contacts.keys()):
            res = policy(graph, node, self.filter_rssi, self.filter_duration,self.SOCIOPATTERN)
            if len(self.contacts[node]) == self.memory_contacts:
                self.contacts[node] = self.contacts[node][1:]
                self.contacts[node].append(res)
            else:
                self.contacts[node].append(res)
        

    def update_quarantened(self,current_time):
        for node in list(self.contacts.keys()):
            if node in self.quarantined and current_time - self.quarantined[node]['in_time'] >= self.max_time_quar:
                self.quarantined.pop(node)
                if node in self.I:
                    self.infected.append(node)
        

        






