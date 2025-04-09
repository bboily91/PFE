from UE import liste, crs, data
from grid import make_grid
from pathlib import Path

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd


# Chemin du module
path = Path(__file__).parent.parent

# Produire le DataFrame des correspondances 'point_id' et 'mp_id'
result = pd.read_csv(path / 'result.csv').set_index("point_id")["mp_id"].to_dict()

# Produire le dictionnaire de points
points = make_grid(blocs=liste, data=data)

# Produire nouveau GeoDataFrame
new_points = gpd.GeoDataFrame(data=points, crs=crs)

# Générer une colonne
mp = new_points.apply(lambda x: result[x['point_id']], axis=1)

# Nommer la nouvelle colonne
mp.name = 'mp_id'

# Joindre la colonne 'mp_id' au GeoDataFrame 'mean_points'
new_points = new_points.join(mp)

# Faire la jointure entre la table de la DRF et la couche de points
table = pd.read_csv('~/ULaval/PFE/DRF/E_gaulMP.CSV')
table["bloc_id"] = table["ID__PLACET"].apply(lambda x: f'B{int(x.split('-')[3])}' if isinstance(x, str) and len(x.split('-')) > 3 else None)
x = table.groupby(['bloc_id', 'NO_MICRO_P']).sum('NBRE_GAULE').reset_index()[['bloc_id', 'NO_MICRO_P', 'NBRE_GAULE']]
x.rename(columns={'NO_MICRO_P': 'mp_id', 'NBRE_GAULE': 'nb_gaule'}, inplace=True)
new_points = pd.merge(left=new_points, right=x, on=['bloc_id', 'mp_id'], how="left")

# Générer une colonne 'NB_GAULE_HA'. Pour une placette de 25m carré, le facteur de conversion = 400
new_points['nb_gaule_ha'] = new_points['nb_gaule']*400

# Vérifi si les combinaison 'point_id' et 'bloc_id' est unique dans le geodataframe
is_unique = not new_points.duplicated(subset=['point_id', 'bloc_id']).any()
print(f"La combinaison 'point_id' et 'bloc_id' est unique : {is_unique} \n")

# Exporter en fichier de forme
print(f'Writting "{path}/PFE.gpkg"')
new_points.to_file(path / 'PFE.gpkg', driver='GPKG', layer='grid_equi')

# Plot les nouveaux grid et les coins
ax = new_points.plot(cmap='magma')
data.plot(ax=ax, cmap='cool')
plt.show()
