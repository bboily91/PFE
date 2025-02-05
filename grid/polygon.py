from UE import liste, crs, data
from shapely import Polygon, Point
from pathlib import Path
from grid import finder

import geopandas as gpd
import matplotlib.pyplot as plt


"""
Générer les polygones à partir des quatre points de chaque unité expérimentale (UE)
"""



def make_poly(bloc: list, data: gpd.GeoDataFrame, container: dict) -> dict:
	"""
	Args:
        - blocs (list) ex: [['B18_E', 'B18_N', 'B18_O', 'B18_S'], ...]
        - data (geopandas.GeoDataFrame)

	Return:
		- coin (dict): {'UE_ID': ['UE_1', ...], 'geometry': [Point(x, y), ...]}
	"""

	UE = bloc[0].lstrip('B').rstrip('_NSEO')

	x = data[data['ID_PE'].isin(bloc)].to_dict()

	p1 = finder(dic=x, bloc=bloc, j=0)
	p2 = finder(dic=x, bloc=bloc, j=1)
	p3 = finder(dic=x, bloc=bloc, j=2)
	p4 = finder(dic=x, bloc=bloc, j=3)
	p5 = finder(dic=x, bloc=bloc, j=0)

	poly = Polygon(((p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y), (p5.x, p5.y)))

	container['UE_ID'].append(f'Bloc_{UE}')
	container['geometry'].append(poly)

	return container


# Dictionnaire vide
polygon = {
	'UE_ID': [],
	'geometry': []
}

# Pour chaque liste d'UE
for bloc in liste:
	make_poly(bloc=bloc, data=data, container=polygon)

# Crée un geodataframe à partir du dictionnaire
blocs = gpd.GeoDataFrame(polygon, crs=crs)

# Exporter le geodataframe en GPKG
path = Path(__file__).parent

if not (path / 'poly.gpkg').exists():
	print(f'Writting "{path}/poly.gpkg"')
	blocs.to_file(path / 'poly.gpkg', driver='GPKG', layer='poly')

# Plot les nouveaux polygones
ax = blocs.plot(cmap='magma')
plt.show()
