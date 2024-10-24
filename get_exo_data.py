import requests
import pandas as pd
import io

# Base URL for the TAP service
base_url = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query='

query = 'select+pl_name,ra,dec,sy_dist+from+ps'

# Specify the format (e.g., CSV)
full_url = base_url + query + '&format=csv'

# Send the GET request
response = requests.get(full_url)

# Check if the request was successful
if response.status_code == 200:
    # Use io.StringIO to convert text response to pandas DataFrame
    data = response.text
    df = pd.read_csv(io.StringIO(data))

    # Save DataFrame to a CSV file
    df.to_csv('all_planets_data.csv', index=False)

    print("Data successfully saved to all_planets_data.csv")
else:
    print("Error:", response.status_code)


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
       
df = pd.read_csv('all_planets_data.csv')

exos = []

for index, row in df.iterrows():
    if index == 0:
        continue

    new_exo = Exo(df.iloc[index, 0],df.iloc[index, 1],df.iloc[index, 2], df.iloc[index, 3])
    exos.append(new_exo)


for exo in exos:
    print(f"ID: {exo.get_id()}, Dec: {exo.get_dec()}, RA: {exo.get_dec()}, Dist: {exo.get_dist()}")



