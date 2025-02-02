"""
Prend en charge un fichier CSV contenant les information de la table attributaire
et une colonne 'long' et 'lat'. 

Génère un objet GeoDataFrame et produit un geopackage (ESPG:4326)
"""

from shapely.geometry import Point
from pathlib import Path

import geopandas as gpd
import pandas as pd


# Chemin du module
path = Path(__file__).parent

data = pd.read_csv('data\\donneesLiDAR.csv', sep=';')

geometry = [Point(xy) for xy in zip(data['long'], data['lat'])]

pl = gpd.GeoDataFrame(data=data, geometry=geometry, crs='EPSG:4326')


# Exporter en fichier de forme
if not (path / 'LiDARTerrestre.gpkg').exists():
	print(f'Writting "{path}/LiDARTerrestre.gpkg"')
	new_points.to_file(path / 'LiDARTerrestre.gpkg', driver='GPKG', layer='LiDAR_TER')

