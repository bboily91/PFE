from UE import liste, crs, data
from grid import mean_grid
from pathlib import Path
from shapely import Point

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd


# Chemin du module
path = Path(__file__).parent.parent

# Produire le DataFrame des correspondances 'point_id' et 'mp_id'
result = pd.read_csv(path / 'result.csv').set_index("point_id")["mp_id"].to_dict()

# Produire le dictionnaire de points
points = mean_grid(blocs=liste, data=data)

# Produire nouveau GeoDataFrame
new_points = gpd.GeoDataFrame(data=points, crs=crs)

# Calculer la moyenne des X et Y pour chaque placette
new_points["X"] = new_points["geometry"].apply(lambda p: p.x)
new_points["Y"] = new_points["geometry"].apply(lambda p: p.y)

# Créer un pandas.dataframe en groupant sur les colonne 'point_id' et 'bloc_id'
centroids = new_points.groupby(["point_id", "bloc_id"])[["X", "Y"]].mean().reset_index()
centroids["geometry"] = centroids.apply(lambda row: Point(row["X"], row["Y"]), axis=1)

# Générer un nouveau geodataframe avec le pandas.dataframe 'centroids'
mean_points = gpd.GeoDataFrame(data=centroids[["bloc_id", "point_id", "geometry"]], geometry="geometry", crs="EPSG:26919")

# Générer une colonne
mp = mean_points.apply(lambda x: result[x['point_id']], axis=1)

# Nommer la nouvelle colonne
mp.name = 'mp_id'

# Joindre la colonne 'mp' au GeoDataFrame 'mean_points'
mean_points = mean_points.join(mp)
print(mean_points.head())

# mean_points["mp_id"] = mean_points["mp_id"].apply(lambda x: f'B{int(x.split('-')[3])}' if isinstance(x, str) and len(x.split('-')) > 3 else None)

# Faire la jointure entre la table de la DRF et la couche de points
table = pd.read_csv('~/ULaval/PFE/DRF/E_gaulMP.CSV')
table["bloc_id"] = table["ID__PLACET"].apply(lambda x: f'B{int(x.split('-')[3])}' if isinstance(x, str) and len(x.split('-')) > 3 else None)
x = table.groupby(['bloc_id', 'NO_MICRO_P']).sum('NBRE_GAULE').reset_index()[['bloc_id', 'NO_MICRO_P', 'NBRE_GAULE']]
x.rename(columns={'NO_MICRO_P': 'mp_id', 'NBRE_GAULE': 'nb_gaule'}, inplace=True)
mean_points = pd.merge(left=mean_points, right=x, on=['bloc_id', 'mp_id'], how="left")

# Générer une colonne 'NB_GAULE_HA'. Pour une placette de 25m carré, le facteur de conversion = 400
mean_points['nb_gaule_ha'] = mean_points['nb_gaule']*400

# Vérifi si les combinaison 'point_id' et 'bloc_id' est unique dans le geodataframe
is_unique = not mean_points.duplicated(subset=['point_id', 'bloc_id']).any()
print(f"La combinaison 'point_id' et 'bloc_id' est unique : {is_unique} \n")

# Exporter en fichier de forme
print(f'Writting "{path}/PFE.gpkg"')
mean_points.to_file(path / 'PFE.gpkg', driver='GPKG', layer='grid_mean')

# Plot les nouveaux grid et les coins
ax = mean_points.plot(cmap='magma')
data.plot(ax=ax, cmap='cool')
plt.show()