#%% System definition
# This files is used to define all the parameters of the model
# It is used for both the simulation of the continuous model and of 
# particle model.


#%%
import numpy as np
from scipy.special import erf


def omega(tau):
    # A Weibull distribution with the given shape and scale
    shape = 2.826
    scale = 5.665
    return (shape / scale) * (tau / scale) ** (shape - 1) * np.exp(-(tau / scale) ** shape)


#%% Infectiousness at time tau
# It requires: 0 <= beta(tau) <= 1
def beta(tau):
    R0 = 2
    return R0 * omega(tau)
#    return 1e-15 + 0 * tau    

def beta_exposure(e, s=0.03, b=5.1): # input: contact duration in seconds
    # Default values:
    #  s = 0.5 sharpness
    #  b = 7.5 where to bend
    ee = e/60 # convert secnds in minutes
    return 1/(1 + np.exp(-s*ee + b))

def beta_exposure_alain(e, beta_t=0.002): # input:  contact duration in seconds
    # Default values:
    dt = 60
    N = e / dt
    return 1 - (1 - beta_t) ** N


def convert_dist_to_s(dist): # it converts the dist in 
    a = 8.851e+05
    c = 113.4
    d = 3.715
    return (a/dist)**(1./d)-c

def convert_s_to_dist(x): # fit fatto con Matlab da Sune (migliorabile)
    a = 8.851e+05
    c = 113.4
    d = 3.715
    return a*1/(x+c)**d

def beta_dist_sign(ss): # input: signal strength. Convert to distance (meters) and then return infection probability
    d = convert_s_to_dist(ss)
    s = 1.5 # increas to increase sharpness (will affect bending point)
    b = 6.6 # increase to move bending to the right
    return 1-1/(1 + np.exp(-s*d + b))

def beta_data(tau, ss, e,beta_t,omega=omega, beta_exposure_alain=beta_exposure_alain, beta_dist_sign=beta_dist_sign): # input: tau (days), signal strength (dBm), esposure (seconds)
#    print("omega",omega(tau))
#    print("e",beta_exposure(e))
#    print("ss",beta_dist_sign(ss))
    return omega(tau) * beta_exposure_alain(e,beta_t) * beta_dist_sign(ss)




def beta_data_sociopattern(tau, e): # input: tau (days), esposure (seconds)
    return omega(tau)*beta_exposure(e)


#%% Probability to become symptomatic once infected, as a function of time
# It requires: 0 <= s(tau) <= 1 with s(tau) a non decreasing function 
MEAN = 1.54          # mean onset time
STD = 0.47           # std onset time
SYMPTOMATICS = 0.8   # number of symptomatic people (old notation: p)
TESTING = 0.25        # perc. of testing of asymptomatics
DELAY = 2            # delay in the reporting (the Merler-factor)

# This is a lognormal distribution with delayed mean, scaled to [0, symptomatics], and then lifted up by relative_testing
# (the sample is converted to seconds)
def onset_time(mean=MEAN, std=STD, symptomatics=SYMPTOMATICS, testing=TESTING, delay=DELAY):  
    relative_testing = (1 - symptomatics) * testing
    return ((symptomatics + relative_testing) * np.random.lognormal(mean, std, size=None) + delay) * 24 * 3600

# 
def s(tau, mean=MEAN, std=STD, symptomatics=SYMPTOMATICS, testing=TESTING, delay=DELAY):
    s_tau_tmp = np.zeros(np.atleast_1d(tau).shape)
    idx_nz = np.nonzero(np.atleast_1d(tau - delay) > 0)
    relative_testing = (1 - symptomatics) * testing
    s_tau_tmp[idx_nz] = .5 + .5 * erf((np.log(np.atleast_1d((tau - delay) / (symptomatics + relative_testing))[idx_nz]) - mean) / (np.sqrt(2) * std))
    s_tau = (symptomatics + relative_testing) * s_tau_tmp
    return s_tau




#%% Control parameters as functions of time
# It requires: 0 <= eps_I, eps_T <= 1 
def epsilon(tau):
    # Constant control parameters
    eps_I = .9 + 0 * tau
    eps_T = .9 + 0 * tau
#    eps_I = tau > 20
#    eps_T = eps_I / 2
#    # Periodic control parameters
#    eps_I = np.cos(tau / np.pi * 1) / 2 + 0.5
#    eps_T = 0.8 * (np.cos((tau - 2) / np.pi * 1) / 2 + 0.5)
    return eps_I, eps_T



#%% Initial number of infected people
Lambda_0 = 10
age = 0


#%% Time grid
T = 50
n_T = 2 * T
tau = np.linspace(0, T, n_T + 1)
delta = tau[-1] - tau[-2]
