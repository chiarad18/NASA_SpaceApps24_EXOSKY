from astroquery.gaia import Gaia
import pandas as pd
from astropy.coordinates import Distance, SkyCoord
from astropy import units as u
import requests
import io

# Query to retrieve all stars from the Gaia catalog
query = """
SELECT TOP 1000
    source_id,
    ra,
    dec,
    parallax
FROM gaiadr3.gaia_source
"""

# Execute the query asynchronously to handle large datasets
job = Gaia.launch_job_async(query)
results = job.get_results()

# Convert the results to a pandas DataFrame
df = results.to_pandas()

# Save the DataFrame to a CSV file
df.to_csv('gaia_star_data.csv', index=False)

print("Data successfully saved to all_star_data.csv")

# Define the Star class
class Star:
    def __init__(self, idnum, ra, dec, dist):
        self._id = idnum
        self._ra = ra
        self._dec = dec
        self._dist = dist

    def get_id(self):
        return self._id

    def get_ra(self):
        return self._ra

    def get_dec(self):
        return self._dec

    def get_dist(self):
        return self._dist


# Load the Gaia star data
df = pd.read_csv('gaia_star_data.csv')

stars = []

# Create Star objects from the CSV file
for index, row in df.iterrows():
    if index == 0:
        continue

    parallax_value = df.iloc[index, 3]
    if pd.isna(parallax_value) or parallax_value == 0.0 or parallax_value < 0:
        continue

    # Create the Star object and calculate distance from parallax
    new_star = Star(
        df.iloc[index, 0],  # source_id
        df.iloc[index, 1],  # ra
        df.iloc[index, 2],  # dec
        Distance(parallax=parallax_value * u.mas)  # parallax to distance
    )
    stars.append(new_star)


# Exoplanet Archive API request to retrieve all exoplanets
base_url = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query='
query = 'select+pl_name,ra,dec,sy_dist+from+ps'
full_url = base_url + query + '&format=csv'

response = requests.get(full_url)

# Check if the request was successful
if response.status_code == 200:
    data = response.text
    df_exo = pd.read_csv(io.StringIO(data))
    df_exo.to_csv('all_planets_data.csv', index=False)
    print("Data successfully saved to all_planets_data.csv")
else:
    print("Error:", response.status_code)


# Define the Exoplanet class
class Exo:
    def __init__(self, idnum, ra, dec, dist):
        self._id = idnum
        self._ra = ra
        self._dec = dec
        self._dist = dist

    def get_id(self):
        return self._id

    def get_ra(self):
        return self._ra

    def get_dec(self):
        return self._dec

    def get_dist(self):
        return self._dist


# Load the exoplanet data
df_exo = pd.read_csv('all_planets_data.csv')

exos = []

# Create Exo objects from the CSV file
for index, row in df_exo.iterrows():
    if index == 0:
        continue

    new_exo = Exo(
        df_exo.iloc[index, 0],  # planet name
        df_exo.iloc[index, 1],  # ra
        df_exo.iloc[index, 2],  # dec
        df_exo.iloc[index, 3]   # distance
    )
    exos.append(new_exo)

# Function to calculate the new RA and Dec of stars relative to an exoplanet
def return_new_stars(exo):
    exoplanet_coord = SkyCoord(ra=exo.get_ra() * u.degree, dec=exo.get_dec() * u.degree, 
                               distance=exo.get_dist() * u.parsec, frame='icrs')
    new_stars = []

    for star in stars:
        star_coord = SkyCoord(ra=star.get_ra() * u.degree, dec=star.get_dec() * u.degree, 
                              distance=star.get_dist().to(u.parsec), frame='icrs')

        # Calculate the star's position relative to the exoplanet
        star_relative_to_exoplanet = star_coord.transform_to(exoplanet_coord.skyoffset_frame())
        
        # Calculate the 3D distance between the star and the exoplanet
        separation = star_coord.separation_3d(exoplanet_coord)

        # Create a new Star object with the relative RA and Dec and 3D separation distance
        new_star = Star(star.get_id(), star_relative_to_exoplanet.lon.deg, 
                        star_relative_to_exoplanet.lat.deg, separation.to(u.parsec))

    
        new_stars.append(new_star)

    return new_stars


# Process first exoplanet

    first_exo = exos[0]
    new_stars = return_new_stars(first_exo)

    for new_star in new_stars:
        print(f"ID: {new_star.get_id()}, RA: {new_star.get_ra()}, Dec: {new_star.get_dec()}, Dist: {new_star.get_dist()}")
