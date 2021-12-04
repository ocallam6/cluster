
import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
import numpy as np
Gaia.MAIN_GAIA_TABLE = "gaiaedr3.gaia_source" # Select early Data Release 3
Gaia.ROW_LIMIT=-1
from astroquery.vizier import Vizier
#Vizier.ROW_LIMIT = -1


def get_clusters()
    try:
        dias = Vizier(catalog="B/ocl/clusters").query_constraints()[0]
        dias=dias[np.argsort(dias['Dist'])]  #assumes that 'dist' is column, just sort
        return dias
    except:
        print('Either catalogue doesnt exist or no column name Dist')
        break
def get_cluster_params(cluster_row):
    try:
        right_as_center=cluster_row['RAJ2000']
        dec_center=cluster_row['DEJ2000']
        diam=cluster_row['Diam']
        return [right_as_center,dec_center,diam]
    except:
        print('column name error')
        break

def gaia_cone_with_distances(right_as_center,dec_center,diam):  #writing diam to remmeber we scan larger than rad
    coord = SkyCoord(right_as_center,dec_center, unit=(u.hourangle, u.deg))
    rad = u.Quantity(diam, u.arcminute)

    r = Gaia.cone_search_async(coordinate=coord, radius=rad, verbose=True)
    
    gaia_edr3=r.get_results()
    gaia_edr3 = gaia_edr3.to_pandas()

    bailer = Vizier.query_region(coord,
                                 radius=rad,
                                 catalog='I/352/gedr3dis')[0]
    bailer=bailer.to_pandas()

    #Gets rid of unmeasured parallax
    gaia_edr3=gaia_edr3[gaia_edr3['parallax']>=-1000] #there is probably a better way of getting rid of the zero values but we shouldnt have that
    
    if((len(gaia_edr3)==len(bailer))and(False not in (gaia_edr3['source_id']==bailer['Source']))):


    else: 
        print('Size difference ')
        break