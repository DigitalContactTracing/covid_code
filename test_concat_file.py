first_input_file = 'RESULTS/actInfs_epsI0_2_initialInfect1_FilRSSI_80_FilDur1200_memCont7_QuarTime10.csv'
second_input_file = 'RESULTS/act_inf_epsI0.2_filterRSSI-73_filterDuration1800.npy'
output_file_npy = 'RESULTS/concat_file_test.npy'
output_file_csv = 'RESULTS/concat_file_test.csv'



from DigitalContactTracing import concat_results

concat_results(first_input_file, second_input_file, output_file_csv)