import os
import numpy as np
import shutil
import yaml

sourcelist = np.genfromtxt("sourceinfo.csv", delimiter=",", dtype=None, encoding='utf-8', unpack=True)
energybins = np.genfromtxt("energybins.csv", delimiter=",", dtype=None, encoding='utf-8', unpack=True)

print(sourcelist[0],energybins)

mainpipeline = '/Volumes/Seagate/Magnetar_Automated_Pipeline/'

# Create Source Folders #
for s in sourcelist[0]:
    print(s)
    new_src_folder = mainpipeline + s
    os.system('mkdir %s'%new_src_folder)

    # Create list.txt Files #
    list_creation_directory = f"{mainpipeline}{s}/"
    filename = "list.txt"
    list_txt_path = os.path.join(list_creation_directory, filename)
    
    photon_folder_directory = f"/Volumes/Seagate/Magnetar_Project/{s}/0p1-300GeV/Photons"
    fits_file_names = os.listdir(photon_folder_directory)

    with open(list_txt_path, 'w') as file:
        for name in fits_file_names:
            list_path = os.path.join(photon_folder_directory, name)
            if name.endswith(".fits") and not name.startswith("._"):
                file.write(list_path + '\n')

    # Create Energy Bin Folders #
    for t in energybins[2]:
        print(t)
        new_bin_folders = os.path.join(new_src_folder, t)
        os.system('mkdir %s'%new_bin_folders)

        # Add Decoy config.yaml File #
        config_source = "config.yaml"
        config_directory = new_bin_folders
        shutil.copy(config_source, config_directory)

        # Edit config.yaml Files #
        config_file_path = os.path.join(new_bin_folders, 'config.yaml')
        with open(config_file_path, 'r') as read_file:
            contents = yaml.safe_load(read_file)
        
        # data: #
        contents["data"]["evfile"] = f"/autobreaux/Magnetar_LAT/{s}/list.txt"

        # selection: #
        ## emin, emax, zmax ##
        if t == "0p1-1GeV":
            contents["selection"]["emin"] = float(100)
            contents["selection"]["emax"] = float(1000)
            contents["selection"]["zmax"] = float(90)
        elif t == "1-10GeV":
            contents["selection"]["emin"] = float(1000)
            contents["selection"]["emax"] = float(10000)
            contents["selection"]["zmax"] = float(105)
        elif t == "0p1-10GeV":
            contents["selection"]["emin"] = float(100)
            contents["selection"]["emax"] = float(10000)
            contents["selection"]["zmax"] = float(90)
        elif t == "0p1-300GeV":
            contents["selection"]["emin"] = float(100)
            contents["selection"]["emax"] = float(300000)
            contents["selection"]["zmax"] = float(90)
        else:
            print("Failure Editing Energy Bins")
            break
        
        ## ra, dec ##
        i = list(sourcelist[0]).index(s)
        contents["selection"]["ra"] = float(sourcelist[1][i])
        contents["selection"]["dec"] = float(sourcelist[2][i])
        
        # model: #
        contents["model"]["sources"] = []
        contents["model"]["sources"].append({
            "name": str(s),
            "ra": float(sourcelist[1][i]),
            "dec": float(sourcelist[2][i]),
            "SpectrumType": 'PowerLaw',  
            "SpatialModel": 'PointSource'  
        })
        
        # Write Changes Into yaml #
        with open(config_file_path, 'w') as write_file:
            yaml.dump(contents, write_file, default_flow_style=False, sort_keys=False)






        




