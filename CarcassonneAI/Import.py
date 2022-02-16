import json
from Tile import Tile
from Feature import *

def importTiles(fpath):
    tileList = []
    f = open(fpath)
    tiles = json.load(f)
    for tile in tiles:
        features = []
        grass = []
        for feat in tile.get('features'):
            if feat.get('City') is not None:
                features.append(City(feat.get('City').get('Edges'), feat.get('City').get('Shield') == "True"))
            elif feat.get('Road') is not None:
                features.append(Road(feat.get('Road').get('Edges'), feat.get('Road').get('Terminated') == "True"))
            elif feat.get('Chapel') is not None:
                features.append(Chapel(None, None))
            elif feat.get('Grass') is not None:
                grass.append(Grass(feat.get('Grass').get('Edges'), False))
        t = Tile(tile.get('id'), features, grass, tile.get('img-code'), 0)
        tileList.append(t)
    f.close()
    return tileList