import json
from Tile import Tile
from Feature import *

def importTiles(fpath):
    tileList = []
    f = open(fpath)
    tiles = json.load(f)
    for tile in tiles:
        features = []
        for feat in tile.get('features'):
            if feat.get('City') is not None:
                features.append(City(feat.get('City').get('Edges'), feat.get('City').get('Shield') == "True"))
            elif feat.get('Road') is not None:
                features.append(Road(feat.get('Road').get('Edges'), feat.get('Road').get('Terminated') == "True"))
            elif feat.get('Chapel') is not None:
                features.append(Chapel(None, None))
        tileList.append(Tile(tile.get('id'), features, tile.get('img-code'), 0))
    f.close()
    return tileList