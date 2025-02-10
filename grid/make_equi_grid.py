from UE import liste, crs, data
from grid import make_grid
from pathlib import Path

import matplotlib.pyplot as plt
import geopandas as gpd


# Chemin du module
path = Path(__file__).parent.parent

# Produire le dictionnaire de points
points = make_grid(blocs=liste, data=data)

# Produire nouveau GeoDataFrame
new_points = gpd.GeoDataFrame(data=points, crs=crs)

# Exporter en fichier de forme
print(f'Writting "{path}/PFE.gpkg"')
new_points.to_file(path / 'PFE.gpkg', driver='GPKG', layer='grid_equi')

# Plot les nouveaux grid et les coins
ax = new_points.plot(cmap='magma')
data.plot(ax=ax, cmap='cool')
plt.show()
