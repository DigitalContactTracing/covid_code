import numpy as np
from scipy.special import erf

# Constants
MEAN = 1.54                      # Mean onset time
STD = 0.47                       # Std onset time
SYMPTOMATICS = 0.8               # Fraction of symptomatic people 
TESTING = 0.25                   # Fraction of testing of asymptomatics
DELAY = 2                        # Delay in the reporting 
Lambda_0 = 1                     # Initial number of infected people
age = 0                          # Max age dist. of initially infected people
T = 50                           # Simulation time
n_T = 2 * T                      # Number of time steps 
tau = np.linspace(0, T, n_T + 1) # Time grid
delta = tau[-1] - tau[-2]        # Time step


def omega(tau):
    """
    Infectiousness probability at time tau.
    
    This functions defines the infection probability as a function of the time
    elapsed since infection. 
    The distribution is a Weibull distribution with the given shape and scale
    
    Parameters
    ----------
    tau: np.array
        time since infection
        
    Returns
    ----------
    p: np.array
        infectiousness probability
    """
    
    shape = 2.826
    scale = 5.665
    p = (shape / scale) * (tau / scale) ** (shape - 1) * np.exp(-(tau / scale) ** shape)
    return p


def beta(tau):
    """
    Infectiousness at time tau, used by the continuous model.
    
    This functions defines the infectiousness as a function of the time
    elapsed since infection. 
    The result is a the value of the infectioun probability, scaled by R0.    
    
    Parameters
    ----------
    tau: np.array
        time since infection
        
    Returns
    ----------
    inf: np.array
        infectiousness
    """

    R0 = 2
    inf = R0 * omega(tau)
    return inf


def beta_exposure(e, beta_t=0.002): # input:  
    """
    Infectiousness as a function of the contact duration.
    
    This functions defines component of the infectiousness that is a function 
    of the duration of a contact in the network.
    
    Parameters
    ----------
    e: float
        contact duration in seconds
    beta_t: float
        istantaneous infection probability (i.e. per unit time)
    
    Returns
    ----------
    val: float
        infectiousness
    """    
    
    dt = 60
    N = e / dt
    val = 1 - (1 - beta_t) ** N
    return val


def beta_dist_sign(ss): # input: signal strength. Convert to distance (meters) and then return infection probability
    """
    Infectiousness as a function of the signal strength.
    
    This functions defines component of the infectiousness that is a function 
    of the signal strenght (roughly: distance) of a contact in the network.
    
    Parameters
    ----------
    ss: float
        signal strenght
    
    Returns
    ----------
    val: float
        infectiousness
    """

    d = convert_s_to_dist(ss)
    s = 1.5 # increas to increase sharpness (will affect bending point)
    b = 6.6 # increase to move bending to the right
    val = 1-1/(1 + np.exp(-s*d + b))
    return val


def beta_data(tau, ss, e, beta_t, omega=omega, beta_exposure=beta_exposure, beta_dist_sign=beta_dist_sign): 
    """
    Infectiousness at time tau, used by the network simulation.
    
    This functions defines the infectiousness as a function of the time
    elapsed since infection, on the distance of a contact, and on the signal 
    strength (if not None) of a contact. 
    
    Parameters
    ----------
    tau: np.array
        time since infection
    ss: float
        signal strenght
    e: float
        contact duration in seconds
    beta_t: float
        istantaneous infection probability (i.e. per unit time)
    omega: function
        probability at time tau
    beta_exposure: function
        infectiousness as a function of the contact duration.
    beta_dist: function
        infectiousness as a function of the signal strength
        
    Returns
    ----------
    val: float
        infectiousness
    """
    
    val = omega(tau) * beta_exposure(e, beta_t)
    if ss != None:
        val *= beta_dist_sign(ss)
    return val


def convert_dist_to_s(dist):
    """
    Convert a distance to a signal strenght.
    
    The function converts a distance to a signal strenght.     
    
    Parameters
    ----------
    dist: float
        distance
        
    Returns
    ----------
    val: float
        signal strength
    """   
    
    a = 8.851e+05
    c = 113.4
    d = 3.715
    val = (a/dist)**(1./d)-c
    return val


def convert_s_to_dist(x): 
    """
    Convert a signal strenght to a distance.
    
    The function converts a signal strength to a distance. The conversion is not
    accurate, and it is only use for the definition of beta_dist.    
    
    Parameters
    ----------
    x: float
        signal strength
        
    Returns
    ----------
    val: float
        distance
    """  
    
    a = 8.851e+05
    c = 113.4
    d = 3.715
    val = a*1/(x+c)**d
    return val


def onset_time(mean=MEAN, std=STD, symptomatics=SYMPTOMATICS, testing=TESTING, delay=DELAY):  
    """
    Sample from the probability distribution of the symptoms onset.
    
    This functions returns a time (days) which is a sample from the 
    distribution that describes the probability for an infected individual to 
    be detected at a certain time, either because it becomes symptomatic, or 
    because it is randomly tested.

    The distribution is a lognormal with delayed mean, scaled to 
    [0, symptomatics], and then lifted up by relative_testing (the sample is 
    converted to seconds).
    
    Parameters
    ----------
    mean: float
        mean onset time
    std: float
        std onset time
    symptomatics: float
        fraction of symptomatic people
    testing: float
        fraction of testing of asymptomatics
    delay: function
        delay in the reporting
        
    Returns
    ----------
    val: float
        time (days) when the person is detected
    """

    relative_testing = (1 - symptomatics) * testing
    val = ((symptomatics + relative_testing) * np.random.lognormal(mean, std, size=None) + delay) * 24 * 3600
    return val


def s(tau, mean=MEAN, std=STD, symptomatics=SYMPTOMATICS, testing=TESTING, delay=DELAY):
    """
    Cumulative probability distribution of the symptoms onset.
    
    This functions returns the probability for an infected individual to be
    detected as infected before time tau (days). The individual may be detected
    either because it becomes symptomatic, or because it is randomly tested.

    It is a CDF of a lognormal distribution with delayed mean, scaled to 
    [0, symptomatics], and then lifted up by relative_testing (the sample is 
    converted to seconds).
    
    Parameters
    ----------
    tau: float
        time (days)
    mean: float
        mean onset time
    std: float
        std onset time
    symptomatics: float
        fraction of symptomatic people
    testing: float
        fraction of testing of asymptomatics
    delay: function
        delay in the reporting
        
    Returns
    ----------
    s_tau: float
        probability to be detected before time tau
    """

    s_tau_tmp = np.zeros(np.atleast_1d(tau).shape)
    idx_nz = np.nonzero(np.atleast_1d(tau - delay) > 0)
    relative_testing = (1 - symptomatics) * testing
    s_tau_tmp[idx_nz] = .5 + .5 * erf((np.log(np.atleast_1d((tau - delay) / (symptomatics + relative_testing))[idx_nz]) - mean) / (np.sqrt(2) * std))
    s_tau = (symptomatics + relative_testing) * s_tau_tmp
    return s_tau


def epsilon(tau):
    """
    Infectiousness at time tau.
    
    This functions defines the infectiousness as a function of the time
    elapsed since infection. 
    The result is a the value of the infectioun probability, scaled by R0.    
    
    Parameters
    ----------
    tau: np.array
        time since infection
        
    Returns
    ----------
    eps_I, eps_T: np.array(s)
        isolation and tracing efficiency
    """
    
    eps_I = .9 + 0 * tau
    eps_T = .9 + 0 * tau
    return eps_I, eps_T



