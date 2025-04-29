import astropy
import astropy.units as u
from astropy.coordinates import SkyCoord
gc = SkyCoord(l=0*u.degree, b=45*u.degree, frame='galactic')
print(gc)
gc.fk5 # FK5 coordinates
from astropy.coordinates import FK5
gc.transform_to('fk5') 
print(gc)
