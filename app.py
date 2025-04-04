import streamlit as st
import sys
import os
import db
import auth
import face_utils
import cv2
import requests

# Configurer la page (DOIT être tout premier appel Streamlit)
st.set_page_config(page_title="Projet 1 - Auth", layout="centered")

# Redirection JS fiable pour Auth0
st.markdown("""
<script>
  const token = new URLSearchParams(window.location.hash.substring(1)).get("access_token");
  if (token) {
    window.location.href = window.location.origin + "/?token=" + token;
  }
</script>
""", unsafe_allow_html=True)

# Imports supplémentaires
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
db.init_db()

st.title("🔐 Authentification - Projet 1")

# Paramètres Auth0
auth0_domain = st.secrets["auth0"]["domain"]
auth0_client_id = st.secrets["auth0"]["client_id"]
redirect_uri = "http://localhost:8501"

# URL de connexion Auth0
login_url = f"{auth0_domain}/authorize?response_type=token&client_id={auth0_client_id}&redirect_uri={redirect_uri}&scope=openid%20profile%20email"

# 🔐 Traitement du token
token = st.query_params.get("token")

if token and 'user' not in st.session_state:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{auth0_domain}/userinfo", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        st.success(f"✅ Connecté avec : {user_info['email']}")
        st.session_state['user'] = user_info['email']
        st.page_link("pages/page_acc.py", label="Accéder au Projet 2", icon="🚀")
    else:
        st.error("❌ Échec de connexion via Auth0.")

# Choix de la méthode d'authentification
method = st.radio("Choisis ta méthode d'authentification :", [
    "Nom d'utilisateur / Mot de passe",
    "Reconnaissance faciale",
    "Connexion via Google/Facebook"
])

# Lien vers inscription
st.page_link("pages/register.py", label="👉 Pas encore de compte ? Inscris-toi ici", icon="📝")

# 🔑 Connexion classique
if method == "Nom d'utilisateur / Mot de passe":
    st.subheader("Connexion classique")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type='password')
    if st.button("Se connecter"):
        user = auth.login_user(username, password)
        if user:
            st.success(f"Bienvenue {username}")
            st.session_state['user'] = username
            st.page_link("pages/page_acc.py", label="Accéder au Projet 2", icon="🚀")
        else:
            st.error("❌ Identifiants invalides.")

# 📸 Connexion par reconnaissance faciale
elif method == "Reconnaissance faciale":
    st.subheader("Connexion par reconnaissance faciale")
    if st.button("📷 Activer la caméra"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            current_desc = face_utils.detect_face_descriptor(frame_rgb)
            if current_desc is not None:
                st.image(frame_rgb, caption="Visage capturé")
                user_found = auth.match_face(current_desc)
                if user_found:
                    st.success(f"Bienvenue {user_found}")
                    st.session_state['user'] = user_found
                    st.page_link("pages/page_acc.py", label="Accéder au Projet 2", icon="🚀")
                else:
                    st.warning("❌ Visage non reconnu.")
            else:
                st.warning("❌ Aucun visage détecté.")
        else:
            st.error("Erreur d'accès à la caméra.")

# Connexion via Auth0
elif method == "Connexion via Google/Facebook":
    st.subheader("Connexion via Google / Facebook (Auth0)")

    if not token:
        st.markdown(f"""
            <a href="{login_url}" target="_self">
                <button style='padding:10px 20px; font-size:16px; background:#4CAF50; color:white; border:none; border-radius:5px;'>🔐 Connexion Google/Facebook</button>
            </a>
        """, unsafe_allow_html=True)

    if 'user' in st.session_state:
        st.success(f"✅ Déjà connecté en tant que {st.session_state['user']}")
        st.page_link("pages/page_acc.py", label="Accéder au Projet 2", icon="🚀")

#  Déconnexion
if 'user' in st.session_state:
    if st.button("🔒 Se déconnecter"):
        st.session_state.clear()
        st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
