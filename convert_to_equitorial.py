import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord

# Load Galactic coordinates from the CSV file
input_csv = "random_galactic_points.csv"  # Input file with (l, b)
output_csv = "random_equatorial_points.csv"  # Output file with (RA, Dec)

# Read the CSV file
df = pd.read_csv(input_csv)

# Extract Galactic coordinates
glon = df["Galactic Longitude (deg)"].values
glat = df["Galactic Latitude (deg)"].values

# Convert to SkyCoord object in Galactic frame
galactic_coords = SkyCoord(l=glon * u.deg, b=glat * u.deg, frame="galactic")

# Convert to Equatorial (RA, Dec)
ra_dec_coords = galactic_coords.transform_to("icrs")

# Create a new DataFrame with only RA and Dec
df_equatorial = pd.DataFrame({
    "Right Ascension (deg)": ra_dec_coords.ra.deg,
    "Declination (deg)": ra_dec_coords.dec.deg
})

# Save to a new CSV file
df_equatorial.to_csv(output_csv, index=False)

print(f"Conversion complete. Results saved in {output_csv}")
