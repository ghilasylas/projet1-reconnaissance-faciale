import numpy as np
import cv2
from skimage.feature import graycomatrix, graycoprops
from mahotas.features import haralick


def glcm(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    co_matrice = graycomatrix(gray, [1], [0], None, symmetric=False, normed=False)
    return [
        float(graycoprops(co_matrice, p)[0, 0])
        for p in ['contrast', 'dissimilarity', 'correlation', 'homogeneity', 'ASM', 'energy']
    ]

def haralick_feat(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    features = haralick(gray).mean(0).tolist()
    return [float(x) for x in features]

def bitdesk_feat(image):
    orb = cv2.ORB_create()
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    if descriptors is not None:
        return descriptors.flatten()[:128]
    else:
        return np.zeros(128)

def concat(image):
    v1 = np.array(glcm(image))
    v2 = np.array(haralick_feat(image))
    v3 = np.array(bitdesk_feat(image))
    return np.concatenate([v1, v2, v3])
