import os
import cv2
import numpy as np
from modules.descripteurs import glcm, haralick_feat, bitdesk_feat, concat

def extract_descripteurs_from_dir(folder_path, descripteur_func, output_file):
    signatures = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(folder_path, filename)
            image = cv2.imread(img_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            vecteur = descripteur_func(image)
            signature = np.append(vecteur, filename)
            signatures.append(signature)
            print(f"✔️ {filename} traité")

    np.save(output_file, signatures)
    print(f"✅ Signatures sauvegardées dans {output_file}")