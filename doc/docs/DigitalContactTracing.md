



## DigitalContactTracing

A class that implements digital contact tracing on a real contact network.

The class loads an existing network and simulates the spread of a virus on 
the network, based on the characteristics of an infectious disease. 
At the same time, a digital contact tracing policy is implemented to try to
contain the spread of the virus by enforcing isolation and quarantine, 
depending on the policy specifications.
The class keeps track of a number of relevant quantities (mainly, tracing 
efficacy and histories of quarantined individuals).  

  
Attributes of the class are listed below:


| ATTRIBUTES | Type | Description |
| ------------ | ------------- | ------------ |
| `I` | dict  | details of infected people |
| `infected` | list |infected people|
| `isolated` | list |isolated people|
| `quarantined` | list |quarantined people|
| `symptomatic` | list |symptomatic people|
| `eT` | list |tracing effectivity, per time instant|
| `temporal_gap` | float |temporal gap between static networks|
| `memory_contacts` | int |tracing memory|
| `max_time_quar` | float |quarantine duration |
| `contacts` | list |contacts of each node |
| `sym_t` | list |symptomatic people, full history |
| `iso_t` | list |isolated people, full history |
| `act_inf_t` | list |infected people, full history |
| `q_t` | list |number of quarantined, full history |
| `q_t_i` | list |number of wrongly quarantined, full history |
| `Q_list` | list | quarantined, full history |
| `Qi_lis` | list | wrongly quarantined, full history |
| `sympt` | float | wrongly fraction of symptomatic individuals  |
| `test` | float | wrongly  fraction of asymptomatics who are detected via random testing|
| `eps_I` | float | wrongly  isolation effectivity|
| `filter_rssi` | float | wrongly RSSI threshold of the digital tracing policy |
| `filter_duration` | float | wrongly duration threshold of the digital tracing policy |
| `graphs` | list | snapshots of the temporal graph|
| `beta_t` | float | parameter defining the infectiousness probability |
| `use_rssi` | bool | flag to decide if the simulation is on a SocioPattern dataset |
| `Y_i_nodes` | list | initially infected nodes |
| `NC_nodes` | list | nodes who do not use the app |


   
   
  
Methods of the class are listed below:

| METHODS  | Description |
| ------------ | ------------- |
| [`spread_infection`](DigitalContactTracing/#spread_infection)(graph, node, new_infected, current_time)  | Propagates the infection from an infected node to its neighbors.|
| [`enforce_policy`](DigitalContactTracing/#enforce_policy)(current_time,node,in_quarantine)  |Updates the state of symptomatic people. |
| [`inizialize_contacts`](DigitalContactTracing/#inizialize_contacts)(graph)  |Initialize the contacts from the temporal graph. |
| [`inizialize_infected_time0`](DigitalContactTracing/#inizialize_infected_time0)()  | Initialize the status of the initial infected people. |
| [`policy`](DigitalContactTracing/#policy)(graph, node)  |  Implements a policy on a node in a graph. |
| [`simulate`](DigitalContactTracing/#simulate)()  |  Runs the simulation. |
| [`update_contacts`](DigitalContactTracing/#update_contacts)(graph)  |  Updates the list of traced contacts. |
| [`update_quarantined`](DigitalContactTracing/#update_quarantined)(current_time)  |  Update the list of quarantined people. |
| [`update_infected`](DigitalContactTracing/#update_infected)( current_time, graph, new_infected) | Updates the state of the infected nodes.|
| [`check_quarantined`](DigitalContactTracing/#check_quarantined)( current_time) | Check the status of quarantined nodes.|



## spread_infection

    does_not_have_symptoms_or_not_caught(graph, node, new_infected, current_time)

Propagates the infection from an infected node to its neighbors.

The method loops over the neighbors of an infected node and selectively 
propagates the infection (i.e., add the neighbors to the list of 
infected nodes). 
To decide if the infection is propagated or not, the method checks the 
duration and proximity of a contact and the infection probability 
beta_data.  

**INPUT**  

* graph - a netwrokx graph
* node - the id of the node under consideration
* new_infected - list of pearson newely infected 
* current_time - float representig the current time of the simulation  


## enforce_policy

    enforce_policy(current_time,node,in_quarantine)


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
         

**INPUT**  

* node - the id of the node under consideration
* in_quarantine - boolean flag that specify if the pearson is already qurantained and he/she shows simptoms 
* current_time - float representig the current time of the simulation  



  

## inizialize_contacts

    inizialize_contacts(graph)

Initialize the contacts from the temporal graph.  

**INPUT**  

* graph - a netwrokx graph





## inizialize_infected_time0

    inizialize_infected_time0(graph)

Initialize the status of the initial infected people. 


  

## policy

    policy(graph, node)

Implements a policy on a node in a graph.

**INPUT**  

* graph - a netwrokx graph
* node - the id of the node under consideration


  

## simulate

    simulate()

Runs the simulation.

  

## update_contacts

    update_contacts(current_time)

Update the list of quarantined people

**INPUT**  

* current_time - float representig the current time of the simulation  




## update_infected

    update_infected( current_time, graph, new_infected)

Updates the state of the infected nodes.

The method updates the state of each infected node by advancing in time
its information and by checking if it has become symptomatic.
Moreover, an infected node may be isolated according to the isolation 
efficiency: If it is not isolated, it spread the infection to its 
neighbors; If it is isolated, the tracing policy is enforced on its 
contacts.

**INPUT**  

* current_time - float representig the current time of the simulation  
* graph - Netwrokx graphs 
* new_infected - list of pearson newely infected 



## check_quarantined

    check_quarantined(current_time)

Check the status of quarantined nodes.

The method checks if a nodes becomes symptomatic while in quarantine, and in this case the tracing policy is enforced on its contacts.

**INPUT**  

* current_time - float representig the current time of the simulation  




## UTILITIES

## store_real_time

    store_real_time(res,PARAMETERS,filter_rssi,filter_duration,eps_I)

Store the results of the simulation at the end of each single iteration.
If the file does not exists, it create the file, otherwise it append the current results to the file.

**INPUT**  

* res - list that contains the output of the simulation
* PARAMETERS - dict containing all the parameters of the simulation (se the examples Digital-Contact-Tracing on SocioPattern.ipynb and Digital-Contact-Tracing on DTU.ipynb)
* filter_rssi - float  wrongly RSSI threshold of the digital tracing policy 
* filter_duration - float  wrongly duration threshold of the digital tracing policy
* eps_I - float wrongly  isolation effectivity

## load_results

    load_results(path,file,eps_I,filter_rssi,filter_duration)

Load stored results

**INPUT**  

* path - string representing the path in which results are stored
* file - string specifing the file to load. One of the follow:
    - `q_t`  number of quarantined
    - `q_t_i` number of wrongly quarantined
    - `Q_list` list  of quarantined
    - `Qi_lis` list of wrongly quarantined
    - `I` dict  with details of infected people 
    - `sym_t` list of symptomatic people
    - `iso_t` list of isolated people
    - `act_inf_t` list of infected people
* eps_I - float wrongly  isolation effectivity
* filter_rssi - float  wrongly RSSI threshold of the digital tracing policy 
* filter_duration - float  wrongly duration threshold of the digital tracing policy

**OUTPUT**

* An array containing the loaded results.