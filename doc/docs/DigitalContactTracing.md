



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
| `memory_contacts` | int |tracing memory|
| `q_t` | list |number of quarantined, full history |
| `q_t_i` | list |number of wrongly quarantined, full history |
| `Q_list` | list | quarantined, full history |
| `Qi_lis` | list | wrongly quarantined, full history |
| `sympt` | float | wrongly fraction of symptomatic individuals  |
| `test` | float | wrongly  fraction of asymptomatics who are detected via random testing|
| `eps_I` | float | wrongly  isolation effectivity|
| `filter_rssi` | float | wrongly RSSI threshold of the digital tracing policy |
| `filter_duration` | float | wrongly duration threshold of the digital tracing policy |
| `graphs` | Netwrokx graphs | snapshots of the temporal graph|
| `beta_t` | float | parameter defining the infectiousness probability |
| `SOCIOPATTERN` | bool | flag to decide if the simulation is on a SocioPattern dataset |
| `Y_i_nodes` | list | initially infected nodes |
| `NC_nodes` | list | nodes who do not use the app |


   
   
  
Methods of the class are listed below:

| METHODS  | Description |
| ------------ | ------------- |
| [`does_not_have_symptoms_or_not_caught`](DigitalContactTracing/#does_not_have_symptoms_or_not_caught)(graph, node, new_infected, current_time)  | Updates the state of asymptomatic (or not tested) people. |
| [`have_symptoms`](DigitalContactTracing/#have_symptoms)(current_time,node,in_quarantine)  |Updates the state of symptomatic people. |
| [`inizialize_contacts`](DigitalContactTracing/#inizialize_contacts)(graph)  |Initialize the contacts from the temporal graph. |
| [`inizialize_infected_time0`](DigitalContactTracing/#inizialize_infected_time0)()  | Initialize the status of the initial infected people. |
| [`policy`](DigitalContactTracing/#policy)(graph, node)  |  Implements a policy on a node in a graph. |
| [`simulate`](DigitalContactTracing/#simulate)()  |  Runs the simulation. |
| [`update_contacts`](DigitalContactTracing/#update_contacts)(graph)  |  Updates the list of traced contacts. |
| [`update_quarantined`](DigitalContactTracing/#update_quarantined)(current_time)  |  Update the list of quarantined people. |



## does_not_have_symptoms_or_not_caught

    does_not_have_symptoms_or_not_caught(graph, node, new_infected, current_time)

Updates the state of asymptomatic (or not tested) people.  

**INPUT**  

* graph - a netwrokx graph
* node - the id of the node under consideration
* new_infected - list of pearson newely infected 
* current_time - float representig the current time of the simulation  


## have_symptoms

    have_symptoms(current_time,node,in_quarantine)

Updates the state of symptomatic people.  

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