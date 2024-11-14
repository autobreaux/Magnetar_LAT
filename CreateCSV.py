import os
import numpy as np
import csv

sourcelist = np.genfromtxt("sourceinfo.csv", delimiter=",", dtype=None, encoding='utf-8', unpack=True)
energybins = np.genfromtxt("energybins.csv", delimiter=",", dtype=None, encoding='utf-8', unpack=True)

mainpipeline = '/Volumes/Seagate/Magnetar_Automated_Pipeline/'

# Create CSV #
with open('results_table.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Loop E-Bins #
    for energy_bin in energybins[2]:

        # Loop through Sources #
        for source in sourcelist[0]:

            new_src_folder = os.path.join(mainpipeline, source)
            new_bin_folder = os.path.join(new_src_folder, energy_bin)

            # Target_results.txt Path #
            txt_file_path = os.path.join(new_bin_folder, 'Target_results.txt')

            # Check for Target_results.txt #
            if os.path.isfile(txt_file_path):
                
                with open(txt_file_path, 'r') as txt_file:
                    rows = [line.strip().split() for line in txt_file]
                    flat_row = [item for sublist in rows for item in sublist]

                    # Write row into CSV #
                    if flat_row:
                        writer.writerow(flat_row)
            else:
                print(f"File not found: {txt_file_path}")
