# Functions Continuous Model

## MidpointNormalize

    MidpointNormalize(colors.Normalize)


Normalise the colorbar.

The function normalises a colorbar so that diverging bars work there way either side from a prescribed midpoint value),
e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))

Source :[Link](https://chris35wills.github.io/matplotlib_diverging_colorbar/)

## time_evolution
    time_evolution(tau, Lambda_0, T, epsilon=epsilon, s=s, beta=beta, age=age)

Simulate the continuous model on a discrete time grid.

The function computes the time evolution of the number of infected people according to the dynamics defined by the continuous model, which is discretized on an equally-spaced time grid. 


**INPUT**  

* tau - np.array time grid
* Lambda_0 - np.array initial number of infected people, with varying infection age
* T - float simulation time
* epsilon - function that returns a (possibly time-dependend) pair (eps_I, eps_T)
* beta - function time-dependent infectiousness
* age - float maximal time since infection of the initially infected people

**OUTPUT**

* np.sum(Lambda, axis=1)[age:] - cumulative distribution of the infected people
* Lambda - time distribution of the infected people 
* A - system evolution matrix   