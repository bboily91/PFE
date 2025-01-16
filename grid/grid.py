from shapely import Point

import geopandas as gpd


# Fonction locale
def finder(dic, bloc, j):
    """
    Fonction pour s'assurer que le bon shapely.Point est attribue au bon point cardinal.

    Args:
      - dic: Objet 'data' sous forme de dictionnaire
      - bloc: Sous liste de blocs. Ex: ['B1_E', 'B1_N', 'B1_O', 'B1_S']
      - j: Indice

    Return: <shapely.Point>
    """
    for i in dic['ID_PE'].items():
        if i[-1] == bloc[j]:
            print(f'Bloc {bloc[j]}: ', dic['geometry'][i[0]])
            return dic['geometry'][i[0]]


def make_grid(blocs: list, data: gpd.GeoDataFrame) -> dict:
    """
    Genere une grille de points tous les 10m orientes dans le sens de l'unite experimentale

    Args:
      - blocs (list) ex: [['B18_E', 'B18_N', 'B18_O', 'B18_S'], ...]
      - data (geopandas.GeoDataFrame)

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


            est = finder(dic=x, bloc=bloc, j=0)
            nord = finder(dic=x, bloc=bloc, j=1)
            ouest = finder(dic=x, bloc=bloc, j=2)
            sud = finder(dic=x, bloc=bloc, j=3)

            print()

            print(100*'=', '\n')

            for i in range(1, 7):

                delta_1_x = sud.x - est.x
                delta_1_y = sud.y - est.y
                delta_2_x = ouest.x - nord.x
                delta_2_y = ouest.y - nord.y

                x1 = ((delta_1_x)/7)*i + est.x
                y1 = ((delta_1_y)/7)*i + est.y
                x2 = ((delta_2_x)/7)*i + nord.x
                y2 = ((delta_2_y)/7)*i + nord.y

                point1 = Point((x1, y1))
                point2 = Point((x2, y2))

                # iter sur points Est vers Nord
                for j in range(1, 7):
                    delta_x = point2.x - point1.x
                    delta_y = point2.y - point1.y

                    x = ((delta_x)/7)*j + point1.x
                    y = ((delta_y)/7)*j + point1.y

                    points['col1'].append(f'point_{i}_{j}')

                    points['geometry'].append(Point((x, y)))

        else:
            continue

    return points

