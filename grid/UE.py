"""
Cree une liste des 4 points formant les UE.

Objets:
    - "liste" ex: (list) [['B18_E', 'B18_N', 'B18_O', 'B18_S'], ...]
    - "crs" ex: EPSG:26919 - NAD83 UTM zone 19N
    - "data" couche de points sous frome de shapefile

"""

import geopandas as gpd


# Raw points
data = gpd.read_file(r'/home/bender/code/autogis/_data/Points_UE_Duchesnay.zip')[['ID_PE', 'geometry']]

# 
crs = data.crs

# Create sorted liste of each point of each UE.
# Only include corner points.
# ============================================
liste = []

for i in range(1, 20):
    y = []
    for j in data['ID_PE']:
        x = j.lstrip('B').split('_')
        num = x[0]
        if num == str(i) and len(x) <= 2 and len(x[1]) == 1:
            y.append(j)
    liste.append(y)

else:
    # Trie la liste en fonction du dernier caractere
    for l in liste:
        l.sort(key=lambda x: x[-1])

# ============================================