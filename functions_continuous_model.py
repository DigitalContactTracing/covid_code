import numpy as np
from system_definition import s, beta, epsilon, age
import matplotlib.colors as colors


def time_evolution(tau, Lambda_0, T, epsilon=epsilon, s=s, beta=beta, age=age):
    """
    Simulate the continuous model on a discrete time grid.
    
    The function computes the time evolution of the number of infected people
    according to the dynamics defined by the continuous model, which is 
    discretized on an equally-spaced time grid.
    
    Parameters
    ----------
    tau: np.array
        time grid
    Lambda_0: np.array
        initial number of infected people, with varying infection age
    T: float
        simulation time
    epsilon: function
        function that returns a (possibly time-dependend) pair (eps_I, eps_T)
    beta: function
        time-dependent infectiousness
    age: float
        maximal time since infection of the initially infected people
        
    Returns
    ----------
    np.sum(Lambda, axis=1)[age:]:
        cumulative distribution of the infected people
    Lambda:
        time distribution of the infected people
    A: 
        system evolution matrix        
    """ 
    
    n = tau.shape[0] - 1
    assert n / T > beta(tau[0]), 'n / T should be larger than beta(tau[0])'
 
    # Evaluate the policy
    eps_I, eps_T = epsilon(tau)
    
    # Compute the matrix A 
    A = np.zeros((n, n))
    for i in range(n):
        c = beta(tau[i]) * (1 - eps_I[i] * s(tau[i]))
        for j in range(n - i): 
            A[i, j] = c  * (1 - eps_T[j] * (s(tau[i] + tau[j]) - s(tau[j])) / (1 - s(tau[j])))    

    # Run the actual time evolution
    Lambda = np.zeros((n, n))  
    Lambda[age, :age+1] = Lambda_0 / (age + 1)
    w = T / n
    for k in range(age + 1, n):
        for i in range(k, 0, -1): # fix this, move to matrix mult. if possible
            Lambda[k, i] = w * A[i, :k-i+1] @ Lambda[k-i, :k-i+1].transpose()
        Lambda[k, 0] = (w * A[0, 1:k] @ Lambda[k, 1:k].transpose())  / (1 - w * A[0, 0])

    # Return Lambda, and its integral lambda
    return np.sum(Lambda, axis=1)[age:], Lambda, A


class MidpointNormalize(colors.Normalize):
	"""
	Normalise the colorbar.
    
    The function normalises a colorbar so that diverging bars work there way 
    either side from a prescribed midpoint value),
	e.g. 
    im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
    
    Source : https://chris35wills.github.io/matplotlib_diverging_colorbar/
	"""
    
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)

	def __call__(self, value, clip=None):
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))