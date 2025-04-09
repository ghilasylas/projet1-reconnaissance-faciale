import numpy as np
import os
from modules.distances import euclidenne, manhattan, chebyshev, canberra

DIST_MAP = {
    "euclidean": euclidenne,
    "manhattan": manhattan,
    "chebyshev": chebyshev,
    "canberra": canberra
}

def Recherche_img(image_vector, path_signatures, distance_name, k=5):
    signatures = np.load(path_signatures, allow_pickle=True)
    results = []
    dist_func = DIST_MAP[distance_name]

    for sig in signatures:
        filename = sig[-1]
        vector = sig[:-1].astype(float)
        d = dist_func(image_vector, vector)
        results.append((filename, d))

    results.sort(key=lambda x: x[1])
    return results[:k]
