import os
import numpy as np

sourcelist = np.genfromtxt("sourceinfo.csv", delimiter=",", dtype=None, encoding='utf-8', unpack=True)
energybins = np.genfromtxt("energybins.csv", delimiter=",", dtype=None, encoding='utf-8', unpack=True)

mainpipeline = '/Volumes/Seagate/Magnetar_Automated_Pipeline/'

# Enter Source Folders #
for s in sourcelist[0]:
    print(s)
    new_src_folder = mainpipeline + s
    os.chdir(new_src_folder)

    # Enter Energy Bin Folders #
    for t in energybins[2]:
        print(t)
        new_bin_folders = os.path.join(new_src_folder, t)
        os.chdir(new_bin_folders)
        os.system('python reload_GT_ROI.py')
        os.chdir('..')
    os.chdir('..')
    