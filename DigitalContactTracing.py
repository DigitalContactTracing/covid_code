import numpy as np
import load_temporal_graph as LTG
from system_definition import onset_time, beta_data, beta_data_He
import networkx as nx
from collections import deque

import json
import csv
import os


class DigitalContactTracing:
    """
    A class that implements digital contact tracing on a real contact network.

    The class loads an existing network and simulates the spread of a virus on
    the network, based on the characteristics of an infectious disease.
    At the same time, a digital contact tracing policy is implemented to try to
    contain the spread of the virus by enforcing isolation and quarantine,
    depending on a policy specification.
    The class keeps track of a number of relevant quantities (mainly, tracing
    efficacy and histories of quarantined individuals).

    Attributes
    ----------
    I: dict
        details of infected people
    infected: list
        infected people
    isolated: list
        isolated people
    quarantined: dict
        quarantined people
    symptomatic: list
        symptomatic people
    eT: list
        tracing effectivity, per time instant
    temporal_gap: float
        temporal gap between static networks
    memory_contacts: int
        tracing memory
    max_time_quar: float
        quarantine duration
    contacts: dict
        contacts of each node
    sym_t: list
        symptomatic people, full history
    iso_t: list
        isolated people, full history
    act_inf_t: list
        infected people, full history
    q_t: list
        number of quarantined, full history
    q_t_i: list
        number of wrongly quarantined, full history
    Q_list: list
        quarantined, full history
    Qi_lis: list
        wrongly quarantined, full history
    sympt: float
        fraction of symptomatic individuals
    test: float
        fraction of asymptomatics who are detected via random testing
    eps_I: float
        isolation effectivity
    filter_rssi: float
        RSSI threshold of the digital tracing policy
    filter_duration: float
        duration threshold of the digital tracing policy
    graphs: list
        snapshots of the temporal graph
    beta_t: float
        parameter defining the infectiousness probability
    A_policy: list of sparse matrices
        adjacency matrices where only 'at risk' contacts are stored
    use_rssi: bool
        flag to decide if the dataset has or not rssi information
    Y_i_nodes: list
        initially infected nodes
    NC_nodes: list
        nodes who do not use the app


    Methods
    -------
    __init__(self, graphs, PARAMETERS, eps_I, filter_rssi, filter_duration, use_rssi=True)
        Constructor.

    check_quarantined(current_time)
        Check the status of quarantined nodes.

    spread_infection(graph, node, new_infected, current_time)
        Propagates the infection from an infected node to its neighbors.

    enforce_policy(current_time,node,in_quarantine)
        Update the state of a symptomatic node and quarantine its contacts.

    initialize_contacts(graphs)
        Initialize the contacts from the temporal graph.

    initialize_infected_time0()
        Initialize the status of the initial infected people.

    policy(graph, node):
        Implement a policy on a node in a graph.

    simulate()
        Run the simulation.

    update_contacts(graph)
        Update the list of traced contacts.

    update_infected(current_time, graph, new_infected)
        Updates the state of the infected nodes.

    update_quarantined(current_time)
        Update the list of quarantined people.
    """


    def __init__(self, graphs, PARAMETERS, eps_I, filter_rssi, filter_duration, A_policy, use_rssi=True):
        """
        Constructor.

        The method defines the setup for the simulations.

        Parameters
        ----------
        graphs: list
            snapshots of the temporal graph
        PARAMETERS: dict
            parameters defining the simulation
        eps_I: float
            isolation effectivity
        filter_rssi: float
            RSSI threshold of the digital tracing policy
        filter_duration: float
            duration threshold of the digital tracing policy
        A_policy: list of sparse matrices
            adjacency matrices where only 'at risk' contacts are stored
        use_rssi: bool
            flag to decide if the dataset has or not rssi information
        """

        self.I = dict()
        self.infected = []  # active_infected
        self.isolated = []
        self.quarantined = dict()
        self.symptomatic = []
        self.eT = []
        self.temporal_gap = PARAMETERS["temporal_gap"]
        self.memory_contacts = int(PARAMETERS["memory_contacts"] * 24 * 3600 / self.temporal_gap)
        self.max_time_quar = PARAMETERS["max_time_quar"] * 24 * 3600
        self.contacts = DigitalContactTracing.initialize_contacts(graphs, self.memory_contacts)
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
        self.A_policy = A_policy
        self.use_rssi = use_rssi

        nodes_list = LTG.get_individuals_from_graphs(graphs)
        NC = round(PARAMETERS["nc"]*len(nodes_list)) # nb of non-compliant

        # get infected at time 0
        individuals_0 = list(graphs[0].nodes())
        np.random.shuffle(individuals_0)
        self.Y_i_nodes = individuals_0[0:PARAMETERS["Y_i"]]

        # get people that are using the app
        np.random.shuffle(nodes_list)
        self.NC_nodes = nodes_list[0:NC]

        self.initialize_infected_time0()


    def initialize_infected_time0(self):
        """
        Initialize the status of the initial infected people.

        The method adds the people contained in self.Y_i_nodes to the list I,
        and defines their infectiousness properties.
        """

        for i in self.Y_i_nodes:
            tau = np.random.uniform(0, 10)  # fra 0 e 10 giorni
            self.I[i] = {'tau': tau,
                  'tau_p': None,
                  'to': onset_time(symptomatics=self.sympt, testing=self.test),
                  'inf': [],
                  'e_inf': [],
                  'ss_inf': [],
                  'ss_p': None,
                  'e_p': None}
            self.infected.append(i)


    @staticmethod
    def initialize_contacts(graphs, memory_contacts):
        """
        Initialize the contacts from the temporal graph.

        The method creates a list where the element at position idx is
        the list of contacts of the node idx.
        Each of these lists is initally empty.

        Parameters
        ----------
        graphs: list
            list of static graphs
        memory_contacts: int
            tracing memory

        Returns
        ----------
        contacts: dict
            contacts of each node
        """

        nodes = []
        for g in graphs:
            for n in list(g.nodes()):
                if n not in nodes:
                    nodes.append(n)
        contacts = dict()
        for i in nodes:
            contacts[i] = deque(maxlen=memory_contacts)
        return contacts


    def simulate(self):
        """
        Run the simulation.

        The method runs the simulation on the temporal network.

        Returns
        ----------
        self.eT: list
            tracing effectivity, per time instant
        self.sym_t: list
            symptomatic people, full history
        self.iso_t: list
            isolated people, full history
        self.act_inf_t: list
            infected people, full history
        self.q_t: list
            number of quarantined, full history
        self.q_t_i: list
            number of wrongly quarantined, full history
        Q_nb: list
            number of distict elements in self.Q_list
        Qi_nb: list
            number of distinct elements in self.Qi_list
        self.I: dict
            details of infected people
        """
        # Initialize the simulation time
        current_time = 0

        # Loop over the temporal snapshots
        for time_idx, graph in enumerate(self.graphs):
            # Initialize the list of nodes that are infected at the present time
            new_infected = []

            # Initialize the list of tracing efficacy at the present time
            self.eTt = []

            # Update the tracing contacts
            self.update_contacts(graph, time_idx)

            # Update the state of nodes that are currently in quarantine
            self.update_quarantined(current_time)

            # Update the state of the infected nodes
            self.update_infected(current_time, graph, new_infected)

            # Check if quarantined nodes become symptomatic
            self.check_quarantined(current_time)

            # Update the global tracing efficacy
            if self.eTt != []:
                self.eT.append(np.mean(self.eTt))

            # Update the histories of symptomatics, isolated, infected, ...
            self.sym_t.append(len(self.symptomatic))
            self.iso_t.append(len(self.isolated))
            self.act_inf_t.append(len(self.infected))
            self.q_t.append(len(self.quarantined))
            self.Q_list.extend(self.quarantined.keys())

            # Update the history of false positive (wrongly quarantined)
            q_t_wrongly = 0
            for node in self.quarantined:
                if self.quarantined[node]['infected'] == 'no':
                    q_t_wrongly += 1
                    self.Qi_list.append(node)
            self.q_t_i.append(q_t_wrongly)


            # Advance the simulation time
            current_time = current_time + self.temporal_gap

        Q_nb = len(np.unique(self.Q_list))
        Qi_nb = len(np.unique(self.Qi_list))

        return [self.eT, self.sym_t, self.iso_t, self.act_inf_t, self.q_t, self.q_t_i, [Q_nb], [Qi_nb], self.I]


    def update_infected(self, current_time, graph, new_infected):
        """
        Updates the state of the infected nodes.

        The method updates the state of each infected node by advancing in time
        its information and by checking if it has become symptomatic.
        Moreover, an infected node may be isolated according to the isolation
        efficiency: If it is not isolated, it spread the infection to its
        neighbors; If it is isolated, the tracing policy is enforced on its
        contacts.

        Parameters
        ----------
        current_time: float
            the absolute time since the beginning of the simulation
        graph: networkx.classes.graph.Graph
            snapshots of the temporal graph
        new_infected: list
            nodes that are infected at the current time
        """

        for node in list(self.I.keys()).copy():
            current_to = self.I[node]["to"]
            self.I[node]["tau"] += self.temporal_gap / (3600 * 24) #update tau

            # Becomes sympt.
            if current_to <= current_time:
                if node not in self.symptomatic:
                    self.symptomatic.append(node)

            if node in self.infected:
                r = np.random.uniform(0, 1)

                # If not sympt. or not detected
                if current_to > current_time or r > self.eps_I:
                    self.spread_infection(graph, node, new_infected, current_time)

                # If sympt. or detected
                elif current_to <= current_time and r <= self.eps_I:
                    self.enforce_policy(current_time, node, in_quarantine=False)


    def check_quarantined(self, current_time):
        """
        Check the status of quarantined nodes.

        The method checks if a nodes becomes symptomatic while in quarantine,
        and in this case the tracing policy is enforced on its contacts.

        Parameters
        ----------
        current_time: float
            the absolute time since the beginning of the simulation
        """

        for node in self.quarantined.keys() & self.I.keys():
            current_to = self.I[node]["to"]
            if current_to < current_time:  # symptom onset
                self.enforce_policy(current_time, node, in_quarantine=True)


    def policy(self, time_idx, node):
        """
        Implement a policy on a node in a graph.

        The method gets the neighbors of the node, and for each neighbor it
        applies the policy to decide if it is 'at risk' or not.

        Parameters
        ----------
        time_idx: int
            index of the current time in the list of time instants
        node: int
            a node in the snapshot

        Returns
        ----------
        res: list
            neighbor of nodes which are 'at risk'
        """

        res = list(self.A_policy[time_idx].indices[
                self.A_policy[time_idx].indptr[node]
                :
                self.A_policy[time_idx].indptr[node+1]
                ])
        return res


    def enforce_policy(self, current_time, node, in_quarantine):
        """
        Update the state of a symptomatic node and quarantine its contacts.

        The method updates the state of a node which is found infected, i.e.,
        it is isolated and its contacts are quarantined.
        First, the node is added to the list of isolated nodes and removed from
        the list of infected (if it is not quarantined) or from the list of
        quarantined (if it is quarantined).
        Second, if the node is adopting the app, the list of its past contacts
        which were 'at risk' is processed and each node is quarantined.
        Third, the efficacy of this tracing step is computed and appended to
        the global list self.eTt.

        Parameters
        ----------
        current_time: float
            the absolute time since the beginning of the simulation
        node: int
            a node in the snapshot
        in_quarantine: bool
            whether or not the node is in quarantine
        """

        assert node not in self.isolated # error: isolated

        if not in_quarantine: # if person in quarantine
            assert node not in self.quarantined # error: quar
            assert node in self.infected # error: not inf

            self.isolated.append(node)
            self.infected.remove(node)
        else: # if person non in qurantine
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
                        self.infected.remove(m)  # m is quarantined, so it is not active
                    else:
                        self.quarantined[m] = {'in_time': current_time, 'infected': 'no'}

        if self.I[node]["inf"]:
            eTn = 0
            for inf in self.I[node]["inf"]:  # count how many are left out
                if inf not in C: # Raises a Future warning bec. inf is str, while C is a list of numpy.str_
                    eTn += 1
            eTn /= len(self.I[node]["inf"])
            self.eTt.append(eTn)


    def spread_infection(self, graph, node, new_infected, current_time):
        """
        Propagates the infection from an infected node to its neighbors.

        The method loops over the neighbors of an infected node and selectively
        propagates the infection (i.e., add the neighbors to the list of
        infected nodes).
        To decide if the infection is propagated or not, the method checks the
        duration and proximity of a contact and the infection probability
        beta_data.

        Parameters
        ----------
        graph: networkx.classes.graph.Graph
            snapshots of the temporal graph
        node: int
            a node in the snapshot
        new_infected: list
            nodes that are infected at the current time
        current_time: float
            the absolute time since the beginning of the simulation
        """

        if node in graph:
            for m in graph.neighbors(node):
                if m not in self.I and m not in self.quarantined:
                    e = graph[node][m]["duration"]  # exposure (seconds)
                    if self.use_rssi:
                        ss = graph[node][m]["rssi"]  # signal strength
                    else:
                        ss = None
                    pp = beta_data(self.I[node]['tau'], ss, e, self.beta_t)  # probability of contagion node --> m
                    #pp = beta_data_He(self.I[node]['tau'], ss, e, self.beta_t)  # probability of contagion node --> m

                    rr = np.random.uniform(0, 1)
                    if rr < pp:  # the contagion of m happens
                        to = onset_time(symptomatics=self.sympt, testing=self.test)
                        self.I[m] = {'tau': 0,
                                     'tau_p': self.I[node]['tau'],
                                     'to': current_time + to,
                                     'inf': [],
                                     'e_inf': [],
                                     'ss_inf': [],
                                     'ss_p': ss,
                                     'e_p': e}
                        self.I[node]["inf"].append(m)
                        self.I[node]["e_inf"].append(e)
                        self.I[node]["ss_inf"].append(ss)

                        self.infected.append(m)
                        new_infected.append(m)


    def update_contacts(self, graph, time_idx):
        """
        Update the list of traced contacts.

        The method uses the current snapshot graph to update the list contacts,
        which stores for each node a list of its contacts.
        For each node, the methods finds the neighbor which are 'at risk'
        according to the policy, and adds them to the list of contacts.
        Moreover, the past contacts which are older than the tracing memory are
        discarded.

        Parameters
        ----------
        graph: networkx.classes.graph.Graph
            snapshots of the temporal graph
        time_idx: int
            index of the current time in the list of time instants
        """

        for node in self.contacts:
            res = self.policy(time_idx, node)
            self.contacts[node].append(res) # This is a deque, so elements are
                                            # pop-ed from the left if the length
                                            # exceeds self.memory_contacts


    def update_quarantined(self, current_time):
        """
        Update the list of quarantined people.

        The method finds the nodes who have completed the quarantine time, and
        removes them from the list of quarantined nodes.
        Nodes who are infected at this stage are added to the list of infected
        nodes.

        Parameters
        ----------
        current_time: float
            the absolute time since the beginning of the simulation
        """

        for node in self.contacts.keys() & self.quarantined.keys():
            if current_time - self.quarantined[node]['in_time'] >= self.max_time_quar:
                self.quarantined.pop(node)
                if node in self.I:
                    self.infected.append(node)


# Utilities to save and load the results of the simulation
def store_real_time(res, PARAMETERS, filter_rssi, filter_duration, eps_I):
    """
    Save the results of some simulations.

    The function saves the results of a series of repetitions of a simulation
    with the same set of parameters. The parameters defining the simulation are
    also saved.

    Parameters
    ----------
    res: list
        result of a single simulation, output of DigitalContactTracing.simulate
    PARAMETERS: dict
        parameters defining the simulation
    filter_rssi: : float
        RSSI threshold of the digital tracing policy
    filter_duration: float
        duration threshold of the digital tracing policy
    eps_I: float
        isolation effectivity
    """

    def save_on_csv(filename,variable_list,writing_operation):
        with open(filename, writing_operation) as csvfile:
            writer = csv.writer(csvfile)
            try:
                [writer.writerow(s) for s in variable_list]
            except:
                writer.writerow(variable_list)

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
        np.save(name_I,[results[8]])


def load_results(path, file, eps_I, filter_rssi, filter_duration):
    """
    Load the results of some simulations.

    The function loads the results of a series of repetitions of a simulation
    with the same set of parameters.

    Parameters
    ----------
    path: str
        path of the file to be loaded
    file: str
        name of the file to be loaded
    eps_I: float
        isolation effectivity
    filter_rssi: : float
        RSSI threshold of the digital tracing policy
    filter_duration: float
        duration threshold of the digital tracing policy

    Returns
    ----------
    loaded_file: list
        content of the file
    """

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

    return loaded_file


# Utilities to process a weighted adjacency matrix
from scipy.sparse import csr_matrix

def policy_adjacency_matrix(graphs, filter_duration, filter_rssi, verbose=False):
    '''
    Compute a list of adjacency matrices based on a policy.

    The function computes the adjacency matrix of a list of graph with respect
    to the edge weights (either duration, or duration and rssi), and then it
    applies a policy to decide if a connection is above a threshold specified
    by a policy. The nonzero entries of the matrices are then set to one.

    Parameters:
    ----------
    graphs: list
        snapshots of the temporal graph
    filter_duration: float
        duration threshold of the digital tracing policy
    filter_rssi: float
        RSSI threshold of the digital tracing policy (or None)
    verbose: bool
        flag to decide if info should be printed

    Returns:
    ----------
    A_policy: list of sparse matrices
        adjacency matrices
    '''

    A_policy = []
    if verbose:
        if filter_rssi is not None:
            print('| Duration |  RSSI |  Total |')
        else:
            print('| Duration |  Total |')

    # Get the number of nodes (actually, max id of a node)
    num_nodes = np.max([np.max(graph.nodes) for graph in graphs if len(graph)]) + 1

    # Loop over the temporal snapshots
    for graph in graphs:
        if len(graph):
            # Adjacency duration
            A_duration = nx.adjacency_matrix(graph, weight='duration')
            # Apply filter duration
            A_duration = crop_sparse_matrix(A_duration, filter_duration)
            if filter_rssi is not None:
                # Adjacency rssi
                A_rssi = nx.adjacency_matrix(graph, weight='rssi')
                # Apply filter rssi
                A_rssi = crop_sparse_matrix(A_rssi, filter_rssi)
                # Compute the combined adjacency matrix
                A = A_rssi.multiply(A_duration)
            else:
                A = A_duration

            # Convert the current nodes idx to the global nodes idx
            # Get the nodes idx of the current graph
            nodes_idx = np.array(graph.nodes)
            # Get the locations of the nnz entries and convert them to global idx
            row = nodes_idx[A.nonzero()[0]]
            col = nodes_idx[A.nonzero()[1]]
            # Set data to one (we do not care about the weight)
            data = np.ones(col.shape[0])
            # Define the matrix with global nodes idx
            A_policy.append(csr_matrix((data, (row, col)), shape=(num_nodes, num_nodes)))
        else:
            A_policy.append(csr_matrix(([], ([], [])), shape=(num_nodes, num_nodes)))

        if verbose:
            if filter_rssi is not None:
                print('|     %4d |  %4d |   %4d |' % (A_duration.nnz, A_rssi.nnz, A.nnz))
            else:
                print('|     %4d |   %4d |' % (A_duration.nnz, A.nnz))
    return A_policy


def crop_sparse_matrix(A, threshold):
    '''
    Remove the entries of a sparse matrix that are below a given threshold.

    Parameters:
    ----------
    A: sparse matrix
        a sparse matrix
    threshold: float
        a threshold

    Returns:
    ----------
    A: sparse matrix
        the matrix without the small entries

    Source:
    ----------
    https://seanlaw.github.io/2019/02/27/set-values-in-sparse-matrix/
    '''

    nonzero_mask = np.array(A[A.nonzero()] <= threshold)[0]
    rows = A.nonzero()[0][nonzero_mask]
    cols = A.nonzero()[1][nonzero_mask]
    A[rows, cols] = 0
    A.eliminate_zeros()
    return A
