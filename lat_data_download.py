#!/usr/bin/env python
#------------------------------------------------------------------------------#
#                                                                              #
# Author: Michela Negro, CRESST - NASA/GSFC                                    #
#        Nicolo' DI Lalla, Nicola Omodei - Stanford University                 #
#                                                                              #
#------------------------------------------------------------------------------#


import os
import re
import ast
import time
import yaml
import argparse
import requests
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from importlib.machinery import SourceFileLoader

from utils import download_file

def get_var_from_file(filename):
    f = open(filename)
    global data
    data = SourceFileLoader('data', filename).load_module()
    f.close()

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--analysis_config", type=str, required=True,
        help = "Path to the config file for the LAT data selection")
parser.add_argument("-cat", "--catalog", type=str,
        help = "Path to the catalog with the source coordinates")
parser.add_argument("--upto", type=int, default=1,
                    help = "Taking sources up to this number in the ranking")
parser.add_argument("--srcname", type=str, default=None,
        help = "Name of the specific galaxy; None=all gal in the catalog.")
parser.add_argument("--show", type=ast.literal_eval, choices=[True, False], default=False,
        help = "If True, a map with the source locations will be displayed")
parser.add_argument("--slac", type=ast.literal_eval, choices=[True, False], default=False,
        help = "if True calls the astrowrap script to get fits files from SLAC.")
args = parser.parse_args()

lat_config = args.analysis_config
get_var_from_file(lat_config)

catalog = args.catalog
if catalog.endswith('.csv'): 
    df = pd.read_csv(catalog)
    _name = df['name'].values
    _ra = df['ra'].values
    _dec = df['dec'].values
    _met = df['met'].values
elif catalog.endswith('.yaml'):
    with open(catalog) as file:
        df = yaml.full_load(file) 
        _name = np.array(df['name'])
        _met = np.array(df['met'])
        _ra = np.array(df['ra'])
        _dec = np.array(df['dec'])


if args.show:
    print('Building map of sources...')
    print('\n')

    _ra[_ra>180] =  _ra[_ra>180]-360

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='mollweide')
    plt.title('Sources - Celestial Coordinates')
    ax.scatter(np.radians(_ra), np.radians(_dec))
    plt.grid('on')
    plt.show()
    

if args.srcname is not None:
        
    filename = args.srcname
    iii = np.where(_name == args.srcname)[0]
    ra, dec =  _ra[iii][0], _dec[iii][0]
    print( 'RA, Dec:', ra, dec)

    query_coords = "%.5f, %.5f"%(ra, dec)
    print('Check query coord. string:', query_coords)
    print('\n')
    
    if os.path.exists(filename):
        pass
    else:
        os.mkdir(filename)
      
    if args.slac:
        abs_path_src = os.getcwd() + '/%s'%filename

        os.system('python getLATFitsFiles.py --wdir %s/. --outfile ft1.fits --minTimestamp %.3f --maxTimestamp %.3f --type FT1 --verbose 1 --overwrite 1'%(data.TSTART, data.TSTOP, abs_path_src))
        #os.system('python getLATFitsFiles.py --wdir %s. --outfile ft2.fits --minTimestamp 239557417.000 --maxTimestamp 443059201.000 --type FT2 --verbose 2 --overwrite 1'%abs_path_src)

    else:
        
        os.chdir('%s'%filename)
        if os.path.exists('ft1.txt'):
            print('FT1.txt file already exists! Delete the files if you want to download them again!')
            pass
        else:
            print('\n Downloading data ...\n')

            query_args = {"destination": "query", 
                          "coordfield": query_coords, 
                          "coordsystem": "J2000", 
                          "shapefield": "5.0", 
                          "timefield": "%.3f, %.3f"%(data.TSTART, data.TSTOP), 
                          "timetype": "MET", 
                          "energyfield": "100, 1000000", 
                          "photonOrExtendedOrNone": "Photon", 
                          }
                          #"spacecraft": "off"}
        
            query = requests.post('https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi', data = query_args)
            regex_time = re.search('The estimated time for your query to complete is ([0-9]*) seconds', query.text)
            regex_link = re.search('The results of your query may be found at \<a href\=\"(.*)\"\>', query.text)
            waiting_time = int(regex_time.group(1))/4
            print(f"Waiting time is {regex_time.group(1)} seconds. Starting waiting loop of {waiting_time} seconds.")
    
            for i in range(10):
                time.sleep(waiting_time)
                print("Waiting for query to complete.")
                data_links = requests.get(regex_link.group(1))
                regex_complete = re.search('Query complete', data_links.text)
                if regex_complete is not None:
                    break
                elif i == 5:
                    print('Query did not complete. Ending loop.')

            print('Data link:', data_links)
            regex_latdata = re.findall('wget (https.*?fits)', data_links.text)
            if len(regex_latdata)!=0:
                print(f"Found the following files: {regex_latdata}")
            for filelink in regex_latdata:
                print(f"Downloading {filelink}.")
                download_file(filelink)

            #if query_args['spacecraft'] == 'on':
            #    scfile = [f for f in os.listdir('.') if '_SC00.fits' in f][0]
            #    os.system('mv %s ft2.fits'%scfile)
            #    print('File %s renamed as ft2.fits'%scfile)
            #else:
            #    pass

            # Create a txt file with the list of files FT1
            os.system('ls *PH*.fits > ft1.txt')
            print('Created ft1.txt')
        
  
        os.chdir('..')
        os.system('pwd')

else:
    
    for i, m in enumerate(_name[:args.upto]):
        print(i, m)
    
        filename = m
        ra, dec =  _ra[i], _dec[i]
        print( 'RA, Dec:', ra, dec)
    
        if os.path.exists(filename):
            
            os.chdir(filename)
            os.system('pwd')
            
            if os.path.exists('ft1.txt'):
                print('FT1.txt file already exists! Delete the files if you want to download them again!')
                os.chdir('..')
            else:
                print('This folder is empty: deleting it and moving on. Rerun the command!')
                os.chdir('..')
                os.system('rm -r %s'%filename)
                
            os.system('pwd')
            
            
        else:
            os.mkdir(filename)
            os.chdir('%s'%filename)
            
            print('Download the data with lat_data_download.py')
            
            query_coords = "%.5f, %.5f"%(ra, dec)
            print('Check query coord. string:', query_coords)
            print('\n')


            if os.path.exists('ft1.txt'):
                print('FT1.txt file already exists! Delete the files if you want to download them again!')
                pass
            else:
                print('\n Downloading data ...\n')

                query_args = {"destination": "query", 
                          "coordfield": query_coords, 
                          "coordsystem": "J2000", 
                          "shapefield": "5.0", 
                          "timefield": "239557417, 638106244", 
                          "timetype": "MET", 
                          "energyfield": "100, 1000000", 
                          "photonOrExtendedOrNone": "Photon", 
                          "spacecraft": "off"}
        
                query = requests.post('https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi', data = query_args)
                regex_time = re.search('The estimated time for your query to complete is ([0-9]*) seconds', query.text)
                regex_link = re.search('The results of your query may be found at \<a href\=\"(.*)\"\>', query.text)
                waiting_time = int(regex_time.group(1))/4
                print(f"Waiting time is {regex_time.group(1)} seconds. Starting waiting loop of {waiting_time} seconds.")
    
                for i in range(10):
                    time.sleep(waiting_time)
                    print("Waiting for query to complete.")
                    data_links = requests.get(regex_link.group(1))
                    regex_complete = re.search('Query complete', data_links.text)
                    if regex_complete is not None:
                        break
                    elif i == 5:
                        print('Query did not complete. Ending loop.')

                print('Data link:', data_links)
                regex_latdata = re.findall('wget (https.*?fits)', data_links.text)
                if len(regex_latdata)!=0:
                    print(f"Found the following files: {regex_latdata}")
                for filelink in regex_latdata:
                    if '_SC00' in filelink and query_args['spacecraft'] == 'off':
                        pass
                    else:
                        print(f"Downloading {filelink}.")
                        download_file(filelink)

                if query_args['spacecraft'] == 'on':
                    scfile = [f for f in os.listdir('.') if '_SC00.fits' in f][0]
                    os.system('mv %s ft2.fits'%scfile)
                    print('File %s renamed as ft2.fits'%scfile)
                else:
                    pass

            # Create a txt file with the list of files FT1
            os.system('ls *PH*.fits > ft1.txt')
            print('Created ft1.txt')
        
  
            os.chdir('..')
            os.system('pwd')


