import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Input FITS file
fits_file = '1e_1048.1-5937_lightcurve.fits'

# Load the FITS file
with fits.open(fits_file) as hdul:
    # Display the FITS structure
    hdul.info()
    
    # Assuming the data is in the first extension (index 1)
    data = hdul[1].data
    
    # Extract the relevant columns
    ts = data['ts']  # Replace with the correct column name for time series if needed
    tmin = data['tmin']  # Replace with the correct column name for time in minutes
    flux = data['flux']  # Replace with the correct column name for flux
    eflux = data['eflux']  # Replace with the correct column name for energy flux
    flux_ul95 = data['flux_ul95']
    eflux_ul95 = data['eflux_ul95']

    # Find the second highest tmin and its corresponding index
sorted_indices = np.argsort(tmin)  # Get indices that would sort tmin
second_highest_index = sorted_indices[-2]  # Second highest tmin index

# Extract the tmin and flux_ul95 for the second highest tmin
tmin_second_highest = tmin[second_highest_index]
flux_ul95_second_highest = flux_ul95[second_highest_index]
eflux_ul95_second_highest = eflux_ul95[second_highest_index]

# Plot ts vs. tmin
plt.figure(figsize=(8, 6))
plt.plot(tmin, ts, marker='o', linestyle = 'None', color='b', label='ts vs. tmin')
plt.xlabel('tmin')
plt.ylabel('ts')
plt.title('ts vs. tmin')
plt.grid(True)
plt.legend()
plt.savefig('ts_vs_tmin.png', dpi=300)
plt.show()


###################################


# Plot eflux vs. tmin with the single eflux_ul95 point and arrow
plt.figure(figsize=(8, 6))
plt.plot(tmin, eflux, marker='s', linestyle='None', color='r', label='eflux')

# Plot the single point
plt.scatter(
    tmin_second_highest, eflux_ul95_second_highest,
    color='purple', label='eflux_ul95', zorder=5
)

# Customize the plot
plt.xlabel('tmin')
plt.ylabel('flux')
plt.title('eflux vs. tmin with eflux_ul')
plt.grid(True)
plt.legend()
plt.savefig('eflux_vs_tmin', dpi=300)
plt.show()


#########################################


# Plot flux vs. tmin with the single flux_ul95 point and arrow
plt.figure(figsize=(8, 6))
plt.plot(tmin, flux, marker='s', linestyle='None', color='g', label='flux')

# Plot the single point
plt.scatter(
    tmin_second_highest, flux_ul95_second_highest,
    color='purple', label='flux_ul95', zorder=5
)

# Customize the plot
plt.xlabel('tmin')
plt.ylabel('flux')
plt.title('flux vs. tmin with flux_ul')
plt.grid(True)
plt.legend()
plt.savefig('flux_vs_tmin', dpi=300)
plt.show()

