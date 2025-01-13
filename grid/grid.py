from shapely import Point

import geopandas as gpd


# Fonction locale
def finder(dic, bloc, j):
    for i in dic['ID_PE'].items():
        if i[-1] == bloc[j]:
            print(f'Bloc {bloc[j]}: ', dic['geometry'][i[0]])
            return dic['geometry'][i[0]]


def make_grid(blocs: list, data: gpd.GeoDataFrame) -> dict:
    """
    Genere une grille de points tous les 10m orientes dans le sens de l'unite experimentale

    Args: blocs (list) ex: [['B18_E', 'B18_N', 'B18_O', 'B18_S'], ...]

    Return: (dict) ex:{'col1': ['point_1', ...], 'geometry': [POINT (296364.056 5201126.639), ...]}
    """

    # Initialise un dictionnaire pour accumuler les instances de shapely.Point 
    # pour generer un GeoDataFrame
    points = {
        'col1': [],
        'geometry': []
    }


    # Pour chaque liste dans la liste 'blocs'
    for bloc in blocs:

        if len(bloc) > 1:

            # Cree un sous-ensemble (dict-like) de data correspondant au 4 elements de la liste 'bloc'
            x = data[data['ID_PE'].isin(bloc)].to_dict()

            print('Bloc:', bloc, '\n')
            print('Sous-ensemble:')
            print(x, '\n')

            print('Resultat de la fonction finder(): ')

            est = finder(dic=x, bloc=bloc, j=0)
            nord = finder(dic=x, bloc=bloc, j=1)
            ouest = finder(dic=x, bloc=bloc, j=2)
            sud = finder(dic=x, bloc=bloc, j=3)

            print()

            print(100*'=', '\n')

            for i in range(1, 6):

                delta_x = sud.x - est.x
                delta_y = sud.y - est.y

                x = ((delta_x)/6)*i + est.x
                y = ((delta_y)/6)*i + est.y

                point = Point((x, y))

                # iter sur points Est vers Nord
                for j in range(1, 6):

                    delta_x = nord.x - est.x
                    delta_y = nord.y - est.y

                    x = ((delta_x)/6)*j + point.x
                    y = ((delta_y)/6)*j + point.y

                    points['col1'].append(f'point_{i}_{j}')

                    points['geometry'].append(Point((x, y)))

        else:
            continue

    return points

