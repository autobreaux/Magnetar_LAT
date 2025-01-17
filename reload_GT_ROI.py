from fermipy import utils
utils.init_matplotlib_backend()
from fermipy.gtanalysis import GTAnalysis
import argparse
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from math import *

c = np.load('fit_TS9.npy', allow_pickle=True).flat[0]
sourcename = list(c['sources'].keys())[0]

Ra = c['sources'][sourcename]['ra']
Dec = c['sources'][sourcename]['dec']

# Define SkyCoord for Later Conversion into Gal. Coords. #

coor_icrs = SkyCoord(ra = Ra*u.degree, dec = Dec*u.degree, frame = 'icrs')

h = open('Target_results.txt','w')
h.write(str(sourcename) + '\n')
h.write(str(coor_icrs.galactic.l) + '\n')
h.write(str(coor_icrs.galactic.b) + '\n')
h.write(str(c['config']['selection']['emin']) + '\n')
h.write(str(c['config']['selection']['emax']) + '\n')
h.write(str(c['sources'][sourcename]['dnde_index']) + '\n')
h.write(str(c['sources'][sourcename]['ts']) + '\n')
h.write(str(c['sources'][sourcename]['eflux_ul95']) + '\n')
h.write(str(c['sources'][sourcename]['flux_ul95']) + '\n')
h.close()
