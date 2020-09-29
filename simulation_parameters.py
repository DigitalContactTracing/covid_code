from random import randrange
parameters_dict = {}

parameters_dict[1] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "R0_reduction_factor" : 1.0,          # factor to reduce R0
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60],
               'policy6': [-91, 30*60],
               'policy7': [-70, 5*60]
              },
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.,                           # Fraction of individuals who are not adopting the app
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim1/"}} # Target folder to save the results


parameters_dict[6] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60],
               'policy6': [-91, 30*60],
               'policy7': [-70, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.2,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.001,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim6/"}} # Target folder to save the results


parameters_dict[7] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.4,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.001,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim7/"}} # Target folder to save the results



parameters_dict[9] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.001,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim9/"}} # Target folder to save the results


parameters_dict[10] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.0015,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.8,                 # Fraction of symptomatic individuals
              "testing" : 0.25,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim10/"}} # Target folder to save the results


parameters_dict[15] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60],
               'policy6': [-91, 30*60],
               'policy7': [-70, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.001,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim15/"}} # Target folder to save the results



parameters_dict[16] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 4,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.001,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim16/"}} # Target folder to save the results


parameters_dict[18] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.001,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.8,                 # Fraction of symptomatic individuals
              "testing" : 0.25,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim18/"}} # Target folder to save the results



parameters_dict[23] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.6,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.0015,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim23/"}} # Target folder to save the results



parameters_dict[24] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.6,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.001,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim24/"}} # Target folder to save the results


parameters_dict[25] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.6,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.0009,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim25/"}} # Target folder to save the results


parameters_dict[26] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.8,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.0015,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim26/"}} # Target folder to save the results



parameters_dict[27] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.8,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.001,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim27/"}} # Target folder to save the results


parameters_dict[28] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60],
               'policy2': [-80, 20*60],
               'policy3': [-83, 15*60],
               'policy4': [-87, 10*60],
               'policy5': [-91, 5*60]},
              "eps_Is" : [0.2, 0.5, 0.8, 1.0],        # Isolation effectivity
              "times" : 100,                         # Number of repetition of the simulation
              "seed" : 11,                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.8,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.0009,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": True,            # Save the results?
                       "path_to_store":"RESULTS/sim28/"}} # Target folder to save the results

parameters_dict['R0'] = {"temporal_gap" : 300,                 # Temporal gap between static networks (sec)
              "memory_contacts" : 7,                # Tracing memory (days)
              "max_time_quar" : 10,                 # Quarantine duration (days)
              "policies" :                          # Digital tracing policies [RSSI, duration (sec)]
              {'policy1': [-73, 30*60]},
              "eps_Is" : [0.],                      # Isolation effectivity
              "times" : 800,                         # Number of repetition of the simulation
              "seed" : randrange(100),                          # Random seed
              "Y_i" : 1,                            # Number of initially infected people
              "nc" : 0.,                           # Fraction of individuals who are not adopting the app
              "beta_t": 0.0009,                      # Parameter defining the infectiousness probability
              "symptomatics" : 0.6,                 # Fraction of symptomatic individuals
              "testing" : 0.5,                      # Fraction of asymptomatics who are detected via random testing
              "store":{"to_store": False,            # Save the results?
                       "path_to_store":"RESULTS/findR0/"}} # Target folder to save the results
