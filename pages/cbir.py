import streamlit as st
import numpy as np
import os
from PIL import Image
from modules.descripteurs import glcm, haralick_feat, bitdesk_feat, concat
from modules.distances import euclidenne, manhattan, chebyshev, canberra


st.set_page_config(page_title="Recherche CBIR", layout="centered")

# Vérification d'accès
if 'user' not in st.session_state:
    st.warning("❌ Vous devez être connecté pour accéder à cette page.")
    st.stop()

    
# Chemins
DATASET_DIR = "dataset/"
VECTEURS_DIR = "vecteurs/"

# Mapping descripteurs
DESCRIPTEURS = {
    "GLCM": ("Signatures_glcm.npy", glcm),
    "Haralick": ("Signatures_haralick.npy", haralick_feat),
    "BiT": ("Signatures_bit.npy", bitdesk_feat),
    "Concat (GLCM + Haralick + BiT)": ("Signatures_concat.npy", concat)
}

# Mapping distances
DISTANCES = {
    "Euclidienne": euclidenne,
    "Manhattan": manhattan,
    "Chebyshev": chebyshev,
    "Canberra": canberra
}

# 🖼️ Interface

st.title("🔎 Recherche d’Images par Contenu (CBIR)")

uploaded_file = st.file_uploader("📷 Téléversez une image pour la recherche", type=["jpg", "png", "jpeg"])

col1, col2 = st.columns(2)
with col1:
    desc_choice = st.selectbox("🧬 Choisir un descripteur", list(DESCRIPTEURS.keys()))
with col2:
    dist_choice = st.selectbox("📏 Choisir une distance", list(DISTANCES.keys()))

k = st.slider("🔢 Nombre d'images similaires à retourner", 1, 20, 5)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Image de requête", use_container_width=True)

    # Extraction du vecteur
    extract_func = DESCRIPTEURS[desc_choice][1]
    vecteur_req = extract_func(np.array(image))

    # Chargement signatures
    fichier_sign = os.path.join(VECTEURS_DIR, DESCRIPTEURS[desc_choice][0])
    signatures = np.load(fichier_sign, allow_pickle=True)

    # Calcul des distances
    distances = []
    for sig in signatures:
        nom_fichier = sig[-1]
        vecteur_base = sig[:-1].astype(float)
        d = DISTANCES[dist_choice](vecteur_req, vecteur_base)
        distances.append((nom_fichier, d))

    # Tri croissant
    distances.sort(key=lambda x: x[1])

    # Affichage des résultats
    st.markdown("## 🖼️ Résultats de recherche :")
    cols = st.columns(5)
    for i, (nom, d) in enumerate(distances[:k]):
        img_path = os.path.join(DATASET_DIR, nom)
        with cols[i % 5]:
            st.image(img_path, caption=f"{nom} ({d:.2f})", use_container_width=True)
