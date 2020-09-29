import numpy as np
from scipy.special import erf
import bisect

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
SHAPE = 2.826
SCALE = 5.665
BETA_T = 0.019005287273122673
BETA_B = 6.674121
BETA_S = 1.335329
R0_RED_FACTOR = 1.0
PARAM_R0 = 60.0

def omega(tau,shape=SHAPE,scale=SCALE):
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

    p = (shape / scale) * (tau / scale) ** (shape - 1) * np.exp(-(tau / scale) ** shape)
    return p


def omega_integral(tau,shape=SHAPE,scale=SCALE): # integral of omega_function
    return 1-np.exp(-(tau/scale)**shape)

def omega_discrete(tau,shape=SHAPE,scale=SCALE):
    gap = 300/24/3600 #0.5
    intervals = np.arange(gap,60,gap) # distance intervals between 0 and 20 days, each interval is half day long
    i = bisect.bisect_left(intervals, tau) # find in which interval is tau
    #print(intervals[i],beta_dist_integral(intervals[i], beta_s, beta_b),beta_dist_integral(intervals[i]-gap, beta_s, beta_b))
    val = omega_integral(intervals[i], shape,scale) - omega_integral(intervals[i]-gap, shape,scale)
    #print(val)
    return val


def beta(tau):########## RIVEDERE. DOBBIAMO USRAE LA omega(tau) DISCRETIZZATA?
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

    R0 = 1
    inf = R0 * omega(tau)
    return inf


def beta_exposure(e, beta_t=BETA_T): # input:
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

def beta_dist_function(ss, beta_s=BETA_S, beta_b=BETA_B):
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
    norm = np.log(1+np.exp(beta_b))/beta_s
    val = 1-1/(1 + np.exp(-beta_s*d + beta_b))
    return val/norm


def beta_dist_integral(ss, beta_s=BETA_S, beta_b=BETA_B): # integral of beta_dist_function
    d = convert_s_to_dist(ss)
    return (beta_s*d+np.log(1+np.exp(beta_b))-np.log(np.exp(beta_b)+np.exp(beta_s*d)))/np.log(1+np.exp(beta_b))




def beta_data(tau, ss, e, R0_reduction_factor=R0_RED_FACTOR, param_R0=PARAM_R0, omega=omega_discrete, beta_exposure=beta_exposure, beta_dist_integral=beta_dist_integral):
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

    val = omega_discrete(tau) * beta_exposure(e) * param_R0 * R0_reduction_factor
    if ss != None:
        val *= (1-beta_dist_integral(ss))
    return val




def omega_He(tau):
    """
    Infectiousness probability at time tau.

    This functions defines the infection probability as a function of the time
    elapsed since infection.
    The distribution come from the paper He et al., "Temporal dynamics in viral shedding and transmissibility of COVID-19",
    Nature Medicine, 2020, https://doi.org/10.1038/s41591-020-0869-5

    Parameters
    ----------
    tau: np.array
        time since infection

    Returns
    ----------
    p: np.array
        infectiousness probability
    """
    mu, sigma, shift = [2.08665887, 0.45692759, 2.96129333]
    p = lognormal_dens(tau + shift, mu, sigma)

    return p




def beta_data_He(tau, ss, e, beta_t, omega=omega_He, beta_exposure=beta_exposure,beta_dist_integral=beta_dist_integral):
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

    #val = omega(tau) * beta_exposure(e, beta_t)
    #if ss != None:
    #    val *= beta_dist_sign(ss)
    #return val





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
    delay: float
        delay in the reporting (in days)

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
