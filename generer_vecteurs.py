# generer_vecteurs.py (version récursive avec chemin relatif complet)
from modules.extraction import extract_descripteurs_from_dir
from modules.descripteurs import glcm, haralick_feat, bitdesk_feat, concat
import os
import cv2
import numpy as np

DATASET_DIR = "dataset/"
VECTEURS_DIR = "vecteurs/"

def collecter_images_recurse(folder):
    images = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                chemin = os.path.join(root, file)
                images.append(chemin)
    return images

def extract_descripteurs_from_paths(list_paths, descripteur_func, output_file):
    signatures = []
    for chemin in list_paths:
        print(f"🟡 Traitement : {chemin}")
        image = cv2.imread(chemin)
        if image is None:
            print(f"❌ Erreur chargement image : {chemin}")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        vecteur = descripteur_func(image)
        nom = os.path.relpath(chemin, start=DATASET_DIR).replace("\\", "/")
        signature = np.append(vecteur, nom)
        signatures.append(signature)
        print(f"✅ Vecteur généré pour : {nom} (taille: {len(vecteur)})")

    np.save(output_file, signatures)
    print(f"💾 {len(signatures)} vecteurs sauvegardés dans {output_file}")

# Vérification
print("🔍 Scan récursif du dataset...")
all_images = collecter_images_recurse(DATASET_DIR)
print(f"📂 {len(all_images)} images trouvées dans {DATASET_DIR} (sous-dossiers inclus)")

if all_images:
    print("\n🚀 Extraction descripteurs en cours...\n")

    extract_descripteurs_from_paths(all_images, glcm, VECTEURS_DIR + "Signatures_glcm.npy")
    extract_descripteurs_from_paths(all_images, haralick_feat, VECTEURS_DIR + "Signatures_haralick.npy")
    extract_descripteurs_from_paths(all_images, bitdesk_feat, VECTEURS_DIR + "Signatures_bit.npy")
    extract_descripteurs_from_paths(all_images, concat, VECTEURS_DIR + "Signatures_concat.npy")

    print("\n✅ Tous les fichiers de signatures ont été générés avec succès !")
else:
    print("⛔ Opération annulée : aucun fichier à traiter.")
