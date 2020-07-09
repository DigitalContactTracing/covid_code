#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 13:52:29 2020

@author: gab
"""

import numpy as np
from system_definition import s, beta, epsilon, age

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

