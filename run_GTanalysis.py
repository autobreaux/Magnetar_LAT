'''
Make three iteration of the find sources script.
In the end finds all sources with TS>9 using a PL spectrum.
This is the first step of the pipeline.
'''
from fermipy import utils
utils.init_matplotlib_backend()
from fermipy.gtanalysis import GTAnalysis
import argparse
import numpy as np
from math import *


usage = "usage: %(prog)s [config file]"
description = "Run fermipy analysis chain."
parser = argparse.ArgumentParser(usage=usage, description=description)

parser.add_argument('--config', default = 'config.yaml')
args = parser.parse_args()

gta = GTAnalysis(args.config)
#####################################################
# This runs the gtools: gtselect, gtmktime, gtbin, gtexp, etc. #
gta.setup() 
gta.print_model()

ra0 = gta.config['selection']['ra']
dec0 = gta.config['selection']['dec']
print('--- Printing Target ra, dec:', ra0, dec0, ' ---')

# Setting Freed Parameters #
print('--- Freeing Sources ---')
gta.free_sources(free=False) 
gta.free_source('isodiff', free=True)
gta.free_source('galdiff', free=True)
gta.free_source(gta.roi.sources[0].name, free=True)
gta.free_sources(distance=3.0, free=True)
gta.print_model()

# This runs a fast fit to the ROI #
print('--- Optimizing ---')
gta.optimize()
gta.print_model()

# This eliminates sources with TS < 9 #
print('--- Deleting Sources with TS < 9 and TS = nan ---')
gta.delete_sources(minmax_ts=[None,9.], exclude=['isodiff', 'galdiff', gta.roi.sources[0].name])

# This eliminates sources with TS = nan #
cont = 0
for t in range(len(gta.roi.sources)-2):
	cont = cont
else:
	gta.delete_source(gta.roi.sources[t-cont]['name'])
	cont = cont + 1

gta.print_model()

# IF YOU HAVE TO ADD A SOURCE DO: #
# gta.add_source(namesfg, dict(ra=ra0, dec=dec0, Scale=dict(value=1e3,scale=1.0,max="1e5",min="1e-5"), Index=dict(value=-2.1,scale=1.0,max="0.",min="-10."), Prefactor=dict(value=1.0,scale=1e-13,max="1e5",min="1e-5"), SpectrumType='PowerLaw'),  free=True, init_source=True, save_source_maps=True)
# gta.print_model()
# gta.free_sources(free=True)

# Setting Freed Parameters #
print('--- Freeing Sources ---')
gta.free_sources(free=False) 
gta.free_source('isodiff', free=True)
gta.free_source('galdiff', free=True)
gta.free_source(gta.roi.sources[0].name, free=True)
gta.free_sources(distance=3.0, free=True)
gta.print_model()

# Optimizing again #
print('--- Optimizing #2 ---')
gta.optimize()
gta.print_model()

# Setting Freed Parameters #
print('--- Freeing Sources ---')
gta.free_sources(free=False) 
gta.free_source('isodiff', free=True)
gta.free_source('galdiff', free=True)
gta.free_source(gta.roi.sources[0].name, free=True)
gta.free_sources(distance=3.0, free=True)
gta.print_model()

# Fitting #
print('--- Fitting ---')
gta.fit(optimizer='NEWMINUIT')
gta.print_model()

# Setting Freed Parameters #
print('--- Freeing Sources ---')
gta.free_sources(free=False) 
gta.free_source('isodiff', free=True)
gta.free_source('galdiff', free=True)
gta.free_source(gta.roi.sources[0].name, free=True)
gta.free_sources(distance=3.0, free=True)
gta.print_model()

# This finds new sources with TS > 9 #
print('--- Finding New Sources with TS > 9 ---')
model = {'Index' : 2.0, 'SpatialModel' : 'PointSource'}
sdict = gta.find_sources(model=model, sqrt_ts_threshold=3.0, min_separation=0.5) # tsmap_fitter='tsmap'

# Setting Freed Parameters #
print('--- Freeing Sources ---')
gta.free_sources(free=False) 
gta.free_source('isodiff', free=True)
gta.free_source('galdiff', free=True)
gta.free_source(gta.roi.sources[0].name, free=True)
gta.free_sources(distance=3.0, free=True)
gta.print_model()

# Optimizing again #
print('--- Optimizing #3 ---')
gta.optimize()
gta.print_model()

# Setting Freed Parameters #
print('--- Freeing Sources ---')
gta.free_sources(free=False) 
gta.free_source('isodiff', free=True)
gta.free_source('galdiff', free=True)
gta.free_source(gta.roi.sources[0].name, free=True)
gta.free_sources(distance=3.0, free=True)
gta.print_model()

# Fitting #
print('--- Fitting #2 ---')
gta.fit(optimizer='NEWMINUIT')
gta.print_model()
gta.write_roi('fit_TS9', make_plots=True, save_model_map=True)
gta.tsmap(prefix='TSmap_TS9', make_plots=True, write_fits=True, write_npy=True)

# Printing source flux UL and energy flux UL #
print('--- Upper Limit Values ---')
print(gta.roi.sources[0]['flux_ul95'])
print(gta.roi.sources[0]['eflux_ul95'])

# Perform Extended Analysis #
gta.extension(gta.roi.sources[0].name, spatial_model='RadialDisk')

# Test for SED #
print('--- Test for SED ---')
gta.free_sources(free=False)
gta.print_model()

# gta.free_sources(skydir=gta.roi[gta.roi.sources[0].name].skydir, distance=[3.0], free=True)
# gta.free_source('isodiff', free=False, pars=None)
# gta.free_source('galdiff', free=False, pars=None)
# gta.print_model()

# Building target SED #
print('--Building SED of Target--')
print('Printing Energy Binning')
print(gta.log_energies)
gta.sed(gta.roi.sources[0].name, loge_bins=gta.log_energies[::4], outfile='PSR_SED_Every4.fits',free_background=True,write_npy=True,make_plots=True,write_fits=True)
