from astroquery.gaia import Gaia
import astropy.units as u
from astropy.coordinates import SkyCoord


Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"


coord = SkyCoord(ra=280, dec=-60, unit=(u.degree, u.degree), frame='icrs')

width = u.Quantity(0.1, u.deg)
height = u.Quantity(0.1, u.deg)

r = Gaia.query_object_async(coordinate=coord, width=width, height=height)


Gaia.ROW_LIMIT = -1
r = Gaia.query_object_async(coordinate=coord, width=width, height=height)

r.pprint(max_lines=12, max_width=140)

