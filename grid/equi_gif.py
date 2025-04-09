import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from UE import data
from grid import make_grid, mean_grid


def visualize_grid_with_bands(blocs, data, func):
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

    # Définir l'animation
    def update(frame):
        ax.clear()

        # Dessine les points
        ax.scatter(x_coords[:frame], y_coords[:frame], c='blue', label='Points générés')

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


    ani = FuncAnimation(fig, update, frames=len(x_coords) + 1, interval=200)
    return ani

bloc = [['B18_E', 'B18_N', 'B18_O', 'B18_S']]

equiGrid = visualize_grid_with_bands(blocs=bloc, data=data, func=make_grid)
equiGrid.save('ima/equi_grid.gif', writer='pillow', fps=10)
