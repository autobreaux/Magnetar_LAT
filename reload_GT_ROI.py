from fermipy import utils
utils.init_matplotlib_backend()
from fermipy.gtanalysis import GTAnalysis
import argparse
import numpy as np
from math import *

c = np.load('fit_TS9.npy', allow_pickle=True).flat[0]
sourcename = list(c['sources'].keys())[0]

h = open('Target_results.txt','w')
h.write(str(sourcename) + '\n')
h.write(str(c['config']['selection']['emin']) + '\n')
h.write(str(c['config']['selection']['emax']) + '\n')
h.write(str(c['sources'][sourcename]['dnde_index']) + '\n')
h.write(str(c['sources'][sourcename]['ts']) + '\n')
h.write(str(c['sources'][sourcename]['eflux_ul95']) + '\n')
h.write(str(c['sources'][sourcename]['flux_ul95']) + '\n')
h.close()
