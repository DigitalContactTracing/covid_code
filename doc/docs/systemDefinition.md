## omega

    omega(tau)

Infectiousness probability at time tau.

This functions defines the infection probability as a function of the time elapsed since infection. The distribution is a Weibull distribution with the given shape and scale

**INPUT**  

* tau: np.array - time since infection

**OUTPUTS** 

* p: pandas dataframe - infectiousness probability        





## beta

    beta(tau)

Infectiousness at time tau, used by the continuous model. 

This functions defines the infectiousness as a function of the time
elapsed since infection. The result is a the value of the infectioun probability, scaled by R0.    
     

**INPUT**  

* tau: np.array -  time since infection 

**OUTPUTS** 

* inf: np.array  - infectiousness





## beta_exposure

    beta_exposure(e, beta_t=0.002)

Infectiousness as a function of the contact duration. 

This functions defines component of the infectiousness that is a function of the duration of a contact in the network. 

**INPUT**  

* e: float - contact duration in seconds
* beta_t: float DEFAULT = 0.002 -  istantaneous infection robability (i.e. per unit time)

**OUTPUTS** 

* val: float  - infectiousness





## beta_dist_sign

    beta_dist_sign(ss)

Infectiousness as a function of the signal strength. 

This functions defines component of the infectiousness that is a function of the signal strenght (roughly: distance) of a contact in the network. 

**INPUT**  

* ss: float - signal strenght 

**OUTPUTS** 

* val: float  - infectiousness





## beta_data

    beta_data(tau, ss, e, beta_t, omega=omega, beta_exposure=beta_exposure, beta_dist_sign=beta_dist_sign)

Infectiousness at time tau, used by the network simulation. 

This functions defines the infectiousness as a function of the time elapsed since infection, on the distance of a contact, and on the signal strength (if not None) of a contact. 

**INPUT**  

* tau: np.array - time since infection
* ss: float - signal strenght 
* e: float - contact duration in seconds
* beta_t: float DEFAULT = 0.002 -  istantaneous infection robability (i.e. per unit time)
* omega: function -  probability at time tau
* beta_exposure: function - infectiousness as a function of the contact duration. 
* beta_dist: function - infectiousness as a function of the signal strength

**OUTPUTS** 

* val: float  - infectiousness





## convert_dist_to_s

    convert_dist_to_s(dist)

Convert a distance to a signal strenght. 

The function converts a distance to a signal strenght. 

**INPUT**  

* dist: float - distance 

**OUTPUTS** 

* val: float  - signal strength








## convert_s_to_dist

    convert_s_to_dist(x)

Convert a signal strenght to a distance. 

The function converts a signal strength to a distance. The conversion is not accurate, and it is only use for the definition of beta_dist. 

**INPUT**  

* x: float - signal strength 

**OUTPUTS** 

* val: float  - distance







## onset_time

    onset_time(mean=MEAN, std=STD, symptomatics=SYMPTOMATICS, testing=TESTING, delay=DELAY)

Sample from the probability distribution of the symptoms onset.

This functions returns a time (days) which is a sample from the 
distribution that describes the probability for an infected individual to be detected at a certain time, either because it becomes symptomatic, or because it is randomly tested.

The distribution is a lognormal with delayed mean, scaled to 
[0, symptomatics], and then lifted up by relative_testing (the sample is converted to seconds).

**INPUT**  

* mean: float - mean onset time 
* std: float - std onset time
* symptomatics: float DEFAULT = 0.8  - fraction of symptomatic people 
* testing: float DEFAULT = 0.25  - fraction of testing of asymptomatics 
* delay: float DEFAULT = 2 -  delay in the reporting (in days)

**OUTPUTS** 

* s_tau: float  - probability to be detected before time tau








## epsilon

    epsilon(tau)

Infectiousness at time tau. 

This functions defines the infectiousness as a function of the time
elapsed since infection. The result is a the value of the infectioun probability, scaled by R0.    
    

**INPUT**  

* tau: np.array - time since infection 

**OUTPUTS** 

* eps_I: np.array  - isolation efficiency
* eps_T: np.array  - tracing efficiency



