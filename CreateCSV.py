import os
import numpy as np
import csv

sourcelist = np.genfromtxt("sourceinfo.csv", delimiter=",", dtype=None, encoding='utf-8', unpack=True)
energybins = np.genfromtxt("energybins.csv", delimiter=",", dtype=None, encoding='utf-8', unpack=True)

mainpipeline = '/Volumes/Seagate/Magnetar_Automated_Pipeline/'

# Create CSV #
with open('results_table.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Enter Source Folders #
    for s in sourcelist[0]:
        print(s)
        new_src_folder = os.path.join(mainpipeline, s)

        # Enter Energy Bin Folder 1 #
        for t in energybins[2][0]:
            print(t)
            new_bin_folders = os.path.join(new_src_folder, t)

            # Target_results.txt Path #
            txt_file_path = os.path.join(new_bin_folders, 'Target_results.txt')
            if os.path.isfile(txt_file_path):
                with open(txt_file_path, 'r') as txt_file:
                    # Collect All Lines as a Single Row #
                    rows = [line.strip().split() for line in txt_file]
                    flat_row = [item for sublist in rows for item in sublist]
                    
                    # Write the Row Into CSV #
                    writer.writerow(flat_row)
            else:
                continue
    # Enter Source Folders #
    for s in sourcelist[0]:
        print(s)
        new_src_folder = os.path.join(mainpipeline, s)

        # Enter Energy Bin Folder 2 #
        for t in energybins[2][1]:
            print(t)
            new_bin_folders = os.path.join(new_src_folder, t)

            # Target_results.txt Path #
            txt_file_path = os.path.join(new_bin_folders, 'Target_results.txt')
            if os.path.isfile(txt_file_path):
                with open(txt_file_path, 'r') as txt_file:
                    # Collect All Lines as a Single Row #
                    rows = [line.strip().split() for line in txt_file]
                    flat_row = [item for sublist in rows for item in sublist]
                    
                    # Write the Row Into CSV #
                    writer.writerow(flat_row)
            else:
                continue
    # Enter Source Folders #
    for s in sourcelist[0]:
        print(s)
        new_src_folder = os.path.join(mainpipeline, s)

        # Enter Energy Bin Folder 3 #
        for t in energybins[2][2]:
            print(t)
            new_bin_folders = os.path.join(new_src_folder, t)

            # Target_results.txt Path #
            txt_file_path = os.path.join(new_bin_folders, 'Target_results.txt')
            if os.path.isfile(txt_file_path):
                with open(txt_file_path, 'r') as txt_file:
                    # Collect All Lines as a Single Row #
                    rows = [line.strip().split() for line in txt_file]
                    flat_row = [item for sublist in rows for item in sublist]
                    
                    # Write the Row Into CSV #
                    writer.writerow(flat_row)
            else:
                continue
    # Enter Source Folders #
    for s in sourcelist[0]:
        print(s)
        new_src_folder = os.path.join(mainpipeline, s)

        # Enter Energy Bin Folder 4 #
        for t in energybins[2][3]:
            print(t)
            new_bin_folders = os.path.join(new_src_folder, t)

            # Target_results.txt Path #
            txt_file_path = os.path.join(new_bin_folders, 'Target_results.txt')
            if os.path.isfile(txt_file_path):
                with open(txt_file_path, 'r') as txt_file:
                    # Collect All Lines as a Single Row #
                    rows = [line.strip().split() for line in txt_file]
                    flat_row = [item for sublist in rows for item in sublist]
                    
                    # Write the Row Into CSV #
                    writer.writerow(flat_row)
            else:
                continue
    