import streamlit as st
import sys
import os
import db
import auth
import face_utils
import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
db.init_db()

st.set_page_config(page_title="Inscription", layout="centered")
st.title("📝 Enregistrement d'un nouvel utilisateur")

# Champs d'entrée
username = st.text_input("Nom d'utilisateur")
email = st.text_input("Adresse courriel")
password = st.text_input("Mot de passe", type='password')
capture = st.checkbox("📸 Capturer une photo de votre visage (optionnel)")

# Préparer session pour capturer le visage
if "face_descriptor" not in st.session_state:
    st.session_state["face_descriptor"] = None

# Capture caméra
if capture and st.button("📷 Prendre une photo"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        descriptor = face_utils.detect_face_descriptor(frame_rgb)
        if descriptor is not None:
            st.session_state["face_descriptor"] = descriptor
            st.image(frame_rgb, caption="Visage capturé")
            st.success("✅ Visage détecté avec succès !")
        else:
            st.warning("❌ Aucun visage détecté.")
    else:
        st.error("❌ Erreur de capture vidéo.")

# Enregistrement
if st.button("✅ Enregistrer"):
    descriptor = st.session_state["face_descriptor"]

    if not username or not email or not password:
        st.error("❌ Tous les champs doivent être remplis.")
    else:
        if descriptor is None and capture:
            st.warning("⚠️ Vous avez demandé la capture, mais aucun visage n’a été détecté.")
        success = auth.register_user(username, email, password, descriptor)
        if success == True:
            st.success("✅ Utilisateur enregistré avec succès !")
            st.session_state["face_descriptor"] = None
        elif success == "duplicate":
            st.error("❌ Cet utilisateur ou courriel existe déjà.")
        else:
            st.error("❌ Une erreur est survenue.")


