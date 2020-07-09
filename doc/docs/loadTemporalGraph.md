## load_df

    load_df(file_name, n_individuals=None, n_row=None, seed=None)

Load a dataset into a dataframe.
    
The function reads a dataset representing pairwise interactions between 
individuals. 
If required, the function may crop the dataset by keeping only 
a max number of interactions or a max number of randomly chosen individuals. 

**INPUT**  

* file_name: str - file to be loaded
* n_individuals: int - max number of individuals to keep, or None to load all the individuals
* n_row: int - max number of interactions to keep, or None to load all the interactions
* seed: float - random seed to shuffle the individuals when selecting a subset, or None

**OUTPUTS** 

* df: pandas dataframe - dataset        




## remove_individuals

    remove_individuals(df, n_individuals)
    
Restrict a dataset to a subset of the individuals.

The function crops the dataset df by keeping only the interactions 
involving a set of n_individuals, which are randomly chosen. 

**INPUT**  

* df: pandas dataframe - dataset 
* n_individuals: int - max number of individuals to keep

**OUTPUTS** 

* df: pandas dataframe - dataset




## get_array_of_contacts

    get_array_of_contacts(df, temporal_gap, column_name)
    
Group a temporal dataset into discrete times.
    
The function groups the contacts stored in df into sets corresponding to
contacts happening at the same time window. The time windows are computed
based on temporal-gap.


**INPUT**  

* df: pandas dataframe - dataset 
* temporal_gap: float - timestep between consecutive snapshopt of the temporal dataset

    
**OUTPUTS** 

* static_contacts: list - groups of simultaneous contacts  




## get_individuals

    get_individuals(df)
    
Get the individuals who are present in the dataset.

The function return a list of all the unique individuals who are present in
the dataset.

**INPUT**  

* df: pandas dataframe - dataset 
    
**OUTPUTS** 

* nodes_list: list - individuals in the dataset 




## build_graphs

    build_graphs(static_contacts, temporal_gap)
    
Get the individuals who are present in the dataset.

The function returns a list of graphs, in wich each graph represent 
interactions between nodes.
Each edge has two attributes (rssi and duration), where rssi is the power 
of the bluethoot signal and duration is the cumulative duration of the 
contact between two individuals.
If two users keep interacting for multiple temporal instants, then the rssi
signal is averaged.

**INPUT**  

* static_contacts: list -  groups of simultaneous contacts 
* temporal_gap: float - timestep between consecutive snapshopt of the temporal dataset
    
**OUTPUTS** 

* graphs: list of Networkx graphs - graphs representing the interactions at each temporal instant 




## load_df_socio

    #load_df_socio(file_name, extend=True, n_row=None, seed=None)

Load a sociopattern dataset into a dataframe.

The function reads a dataset representing pairwise interactions between 
individuals. 
If required, the function may crop the dataset by keeping only 
a max number of interactions.
Moreover, the function can extend the dataset in time by appending three
copies of the dataset one after the other.


**INPUT**  

* file_name: str - file to be loaded
* extend: bool - decide if the multiple copies of the datasets are appended in time n_row: int
* n_row: int - max number of interactions to keep, or None to load all the interactions
* seed: float - random seed to shuffle the individuals when selecting a subset, or None

**OUTPUTS** 

* df: pandas dataframe - dataset        




## build_graphs_socio

    #build_graphs_socio(static_contacts, temporal_gap)


Get the graphs representing the interactions at each temporal instant

The function returns a list of graphs, in wich each graph represent 
interactions between nodes.
Each edge has an attribute duration which is the cumulative duration of the 
contact between two individuals.


**INPUT**  

* static_contacts: list - groups of simultaneous contacts 
* temporal_gap: float - timestep between consecutive snapshopt of the temporal dataset


**OUTPUTS** 

* graphs: list of Networkx graphs - graphs representing the interactions at each temporal instant                






## show_animation

    #show_animation(graphs, save=False)


Show an animation of the time evolution of the contact network.

The function shows returns an animation of the time evolution of a temporal
network.


**INPUT**  

* graphs: list of Networkx graphs - graphs representing the interactions at each temporal instant                
* save: bool - return or not an animation object (that can be saved)


**OUTPUTS** 

* ani: matplotlib.animation  - animation object                 









## compute_comulative

    #compute_comulative(graphs)


Computes the static aggregation of a temporal network.

The function computes a static graph obtained by merging all the snaphots 
of a temporal network.


**INPUT**  

* graphs: list of Networkx graphs - graphs representing the interactions at each temporal instant                
* save: bool - return or not an animation object (that can be saved)


**OUTPUTS** 

* cumulative_graphs: Networkx graph  - cumulative static graph                  