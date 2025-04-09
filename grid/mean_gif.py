from matplotlib.animation import FuncAnimation
from UE import data
from grid import make_grid, mean_grid
from pathlib import Path
import geopandas as gpd  # Pour charger le shapefile
import matplotlib.pyplot as plt


# Chemin du module
path = Path(__file__).parent.parent

print(path)

def visualize_grid_with_bands(blocs, data, func, final_points_shapefile=None, layer=None):
    fig, ax = plt.subplots(figsize=(8, 8))
    points = func(blocs, data)  # Appelle ta fonction pour obtenir les points
    geometries = points['geometry']
    
    # Sépare les coordonnées des points
    x_coords = [pt.x for pt in geometries]
    y_coords = [pt.y for pt in geometries]
    
    # Récupérer les points de référence pour tracer des bandes
    bloc_ref = blocs[0]  # Exemple : le premier bloc
    data_ref = data[data['ID_PE'].isin(bloc_ref)]
    corners = data_ref.geometry.tolist()
    
    # Charger le shapefile final si fourni
    final_points = None
    if final_points_shapefile:
        gdf_complet = gpd.read_file(final_points_shapefile, layer=layer)
        final_points = gdf_complet[gdf_complet['bloc_id'].str.contains('B18')]
        
    # Durée supplémentaire pour la frame finale (en nombre de frames)
    final_frame_duration = 30  # à 10 FPS, cela donne 1,5 secondes
    total_frames = len(x_coords) + 1 + final_frame_duration
    
    def update(frame):
        ax.clear()
        
        # Si c'est une frame régulière
        if frame <= len(x_coords):
            # Dessine les points accumulés jusqu'à maintenant
            ax.scatter(x_coords[:frame], y_coords[:frame], c='blue', label='Points générés')
        # Si c'est une frame où on montre le shapefile final
        else:
            # Dessine tous les points générés
            ax.scatter(x_coords, y_coords, c='blue', label='Points générés')
            # Et affiche les points du shapefile final
            if final_points is not None:
                final_points.plot(ax=ax, color='red', marker='*', markersize=50, 
                                 label='Points finaux', alpha=0.7)
        
        # Dessine des bandes (axes de référence)
        if len(corners) == 4:
            est, nord, ouest, sud = corners
            ax.scatter([est.x, sud.x], [est.y, sud.y], c='red')
            ax.scatter([nord.x, ouest.x], [nord.y, ouest.y], c='green')
            
        ax.set_xticks([])  # Supprime les graduations de l'axe X
        ax.set_yticks([])  # Supprime les graduations de l'axe Y
        ax.set_frame_on(False)  # Optionnel : supprime le cadre autour du graphique
        ax.legend()
        ax.grid(False)
        
    ani = FuncAnimation(fig, update, frames=total_frames, interval=50)  # 10 FPS
    return ani

bloc = [['B18_E', 'B18_N', 'B18_O', 'B18_S']]

# Utilisation avec le shapefile final
meanGrid = visualize_grid_with_bands(
    blocs=bloc, 
    data=data, 
    func=mean_grid,
    final_points_shapefile=path / 'PFE.gpkg',
    layer='grid_mean'
)

plt.show()

meanGrid.save(path / 'grid/ima/mean_grid.gif', writer='pillow', fps=15)