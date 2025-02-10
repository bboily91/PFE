import geopandas as gpd
import math

from shapely import Point


# Fonction locale
def finder(dic, bloc, j):
    """
    Fonction pour s'assurer que le bon shapely.Point est attribue au bon point cardinal.

    Args:
      - dic: Objet 'data' sous forme de dictionnaire
      - bloc: Sous liste de blocs. Ex: ['B1_E', 'B1_N', 'B1_O', 'B1_S']
      - j: Indice de for loop

    Return: <shapely.Point>
    """
    for i in dic['ID_PE'].items():
        if i[-1] == bloc[j]:
            print(f'Bloc {bloc[j]}: ', dic['geometry'][i[0]])
            return dic['geometry'][i[0]]


def make_grid(blocs: list, data: gpd.GeoDataFrame) -> dict:
    """
    Genere une grille de points seprares d'environ 10m orientes dans le sens de l'unite 
    experimentale.

    Les deux premiers axes de reference sont Est-Sud (axe 1) et Nord-Ouest (axe 2). Chacun des 
    axes est divise en 7 parts egales et un Point est cree localement a chaque jalon. Donc, 6 
    points sont crees. Un processus iteratif prend chaque pair de points correspondant des axes
    1 et 2 pour diviser cette distance en 7 parts egales et cree un Point a chaque jalon. Cette 
    creation de Point se fait de facon transversale aux axes de references. Ce sont ces points 
    crees transversalement qui sont retournes par la fonction.

    Args:
        - blocs (list) ex: [['B18_E', 'B18_N', 'B18_O', 'B18_S'], ...]
        - data (geopandas.GeoDataFrame)

    Return: 
        - (dict) ex:{
                        'col1': ['point_1_1', 'point_1_2', ...],
                        'bloc_id': ['B1', 'B1', ...]
                        'geometry': [POINT (296364.056 5201126.639), ...]
                    }
    """

    # Initialise un dictionnaire pour accumuler les instances de shapely.Point
    # pour generer un GeoDataFrame
    points = {
        'point_id': [],
        'bloc_id': [],
        'geometry': []
    }


    # Pour chaque liste (bloc) de la liste 'blocs'
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

            bloc_id = (bloc[0].split('_'))[0]

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

                for j in range(1, 7):
                    delta_x = point2.x - point1.x
                    delta_y = point2.y - point1.y

                    x = ((delta_x)/7)*j + point1.x
                    y = ((delta_y)/7)*j + point1.y

                    points['point_id'].append(f'point_{i}_{j}')

                    points['bloc_id'].append(f'{bloc_id}')

                    points['geometry'].append(Point((x, y)))

        else:
            continue

    return points

###################################################################################################


# Fonction locale, génère le point moyen pour chaque groupe de 4 points
def generate_mean():
    pass


def mean_grid(blocs: list, data: gpd.GeoDataFrame) -> dict:
    """
    Args:
        - blocs (list) ex: [['B18_E', 'B18_N', 'B18_O', 'B18_S'], ...]
        - data (geopandas.GeoDataFrame)

    Return: 
        - (dict) ex:{
                        'col1': ['point_1_1', 'point_1_2', ...],
                        'bloc_id': ['B1', 'B1', ...]
                        'geometry': [POINT (296364.056 5201126.639), ...]
                    }
    """

    points = {
        'point_id': [],
        'bloc_id': [],
        'sequence': [],
        'geometry': []
    }

    # Pour chaque liste (bloc) de la liste 'blocs'
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

            bloc_id = (bloc[0].split('_'))[0]

            print()

            print(100*'=', '\n')

            # Round 1
            for i in range(1, 7):

                delta_x = sud.x - est.x
                delta_y = sud.y - est.y

                norme = math.sqrt((delta_x**2) + (delta_y**2))

                x = (delta_x/norme)*i*10 + est.x
                y = (delta_y/norme)*i*10 + est.y

                point = Point((x, y))

                for j in range(1, 7):

                    x = (delta_y/norme)*j*10 + point.x
                    y = (delta_x/norme)*j*(-10) + point.y

                    points['point_id'].append(f'point_{i}_{j}')

                    points['bloc_id'].append(f'{bloc_id}')

                    points['sequence'].append('Est-Sud')

                    points['geometry'].append(Point((x, y)))

            # Round 2
            for i in range(1, 7):

                delta_x = ouest.x - sud.x
                delta_y = ouest.y - sud.y

                norme = math.sqrt((delta_x**2) + (delta_y**2))

                x = (delta_x/norme)*i*10 + sud.x
                y = (delta_y/norme)*i*10 + sud.y

                point = Point((x, y))

                for j in range(1, 7):

                    x = (delta_y/norme)*j*10 + point.x
                    y = (delta_x/norme)*j*(-10) + point.y

                    points['point_id'].append(f'point_{j}_{7-i}')

                    points['bloc_id'].append(f'{bloc_id}')

                    points['sequence'].append('Sud-Ouest')

                    points['geometry'].append(Point((x, y)))


            # Round 3
            for i in range(1, 7):

                delta_x = nord.x - ouest.x
                delta_y = nord.y - ouest.y

                norme = math.sqrt((delta_x**2) + (delta_y**2))

                x = (delta_x/norme)*i*10 + ouest.x
                y = (delta_y/norme)*i*10 + ouest.y

                point = Point((x, y))

                for j in range(1, 7):

                    x = (delta_y/norme)*j*10 + point.x
                    y = (delta_x/norme)*j*(-10) + point.y

                    points['point_id'].append(f'point_{j}_{i}')

                    points['bloc_id'].append(f'{bloc_id}')

                    points['sequence'].append('Ouest-Nord')

                    points['geometry'].append(Point((x, y)))


            # Round 4
            for i in range(1, 7):

                delta_x = est.x - nord.x
                delta_y = est.y - nord.y

                norme = math.sqrt((delta_x**2) + (delta_y**2))

                x = (delta_x/norme)*i*10 + nord.x
                y = (delta_y/norme)*i*10 + nord.y

                point = Point((x, y))

                for j in range(1, 7):

                    x = (delta_y/norme)*j*10 + point.x
                    y = (delta_x/norme)*j*(-10) + point.y

                    points['point_id'].append(f'point_{i}_{7-j}')

                    points['bloc_id'].append(f'{bloc_id}')

                    points['sequence'].append('Nord-Est')

                    points['geometry'].append(Point((x, y)))

        else:
            continue

    return points