# 📸 Projet 2 - CBIR (Content-Based Image Retrieval) avec Streamlit

## 🎯 Objectif
Développer une application web complète permettant aux utilisateurs de :
- S'authentifier via nom d'utilisateur/mot de passe, reconnaissance faciale ou Google/Facebook (Auth0)
- Envoyer une image de requête
- Obtenir les **k images les plus similaires** depuis un dataset, en comparant leur contenu visuel

## 🧠 Fonctionnalités principales
- 🔐 Authentification sécurisée multi-méthodes
- 🧬 Descripteurs d'image : GLCM, Haralick, ORB (BiT), Concat
- 📏 Distances : Euclidienne, Manhattan, Chebyshev, Canberra
- 🖼️ Interface utilisateur moderne avec Streamlit
- 📁 Gestion de dataset, extraction et recherche d'images par similarité

## 🗂️ Organisation du projet
```
Projet2_CBIR/
├── app.py                        # Point d'entrée principal Streamlit
├── db.py                         # Connexion SQLite
├── auth.py                       # Gestion utilisateurs / Auth0
├── face_utils.py                 # Reconnaissance faciale
├── requirements.txt              # Dépendances
├── generer_vecteurs.py           # Script de génération des signatures
├── .streamlit/
│   └── secrets.toml              # ⚠️ Clés Auth0 
├── dataset/                      # Dossier contenant les images
├── vecteurs/                     # Dossier contenant les .npy générés
├── modules/
│   ├── descripteurs.py
│   ├── distances.py
│   ├── extraction.py
│   └── recherche.py
├── pages/
│   ├── cbir.py                   # Interface CBIR principale
│   ├── register.py               # Inscription
│   ├── profil.py                 # Profil utilisateur
│   └── aide.py                   # Page d'aide
```

## ▶️ Lancer l'application
### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Générer les fichiers de signatures (facultatif si déjà faits)
```bash
python generer_vecteurs.py
```

### 3. Lancer Streamlit
```bash
streamlit run app.py
```


## 👤 Compte de test
| Nom d'utilisateur | Mot de passe |
|--------------------|--------------|
| `ghilas`           | `123`     |


## 🔬 Technologies utilisées
- Python 3
- Streamlit
- OpenCV, NumPy, scikit-image, mahotas
- Auth0 pour la connexion Google/Facebook



## 🛡️ Sécurité
- Les mots de passe sont hashés avec SHA-256
- Le fichier `.streamlit/secrets.toml` est ignoré par Git pour protéger les clés Auth0

## 📬 Auteur
Projet réalisé par **Ghilas** dans le cadre du cours :
**IA2 – Vision Artificielle et Reconnaissance de Formes (Session 5 - Teccart)**
