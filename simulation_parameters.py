parameters_dict = {}

"""
1: R0 = 3, delay = 2
    
    
"""


parameters_dict[1] = {
              "temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "R0_reduction_factor" : 1.0,          # Factor to reduce R0
              "delay": 2,                           # Delay in the reporting
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60],
               'policy6': [-91, 30*60],
               'policy7': [-70, 5*60]
              },
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],      # Isolation effectivity
              "times" : 100,                        # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.,                            # Fraction of individuals who are not adopting the app
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim1/"}} # Target folder to save the results
