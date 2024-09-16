"""
Prend en charge un fichier CSV contenant les information de la table attributaire
et une colonne 'long' et 'lat'. 

Génère un objet GeoDataFrame et produit un shapefile (ESPG:4326)
"""

from shapely.geometry import Point
import geopandas as gpd
import pandas as pd


data = pd.read_csv('data\\donneesLiDAR.csv', sep=';')

geometry = [Point(xy) for xy in zip(data['long'], data['lat'])]

pl = gpd.GeoDataFrame(data=data, geometry=geometry, crs='EPSG:4326')

pl.to_file(r'C:\Users\Ben\Documents\PFE\LiDARTerrestre.shp')
