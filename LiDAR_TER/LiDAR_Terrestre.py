"""
Prend en charge un fichier CSV contenant les information de la table attributaire
et une colonne 'long' et 'lat'. 

Génère un objet GeoDataFrame et produit un geopackage (EPSG:26919)
"""

from shapely.geometry import Point
from pathlib import Path

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


# Chemin du module
path = Path(__file__).parent.parent

data = pd.read_csv('donneesLiDAR.csv', sep=';')

geometry = [Point(xy) for xy in zip(data['long'], data['lat'])]

pl = gpd.GeoDataFrame(data=data, geometry=geometry, crs='EPSG:26919')


# Exporter en fichier de forme
print(f'Writting "{path}/PFE.gpkg"')
pl.to_file(path / 'PFE.gpkg', driver='GPKG', layer='LiDAR_TER')

ax = pl.plot(cmap='magma')
plt.show()
