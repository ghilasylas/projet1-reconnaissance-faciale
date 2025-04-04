
from db import get_connection
import hashlib
import pickle
import numpy as np
import sqlite3

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password, face_descriptor=None):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    blob = pickle.dumps(face_descriptor) if face_descriptor is not None else None

    try:
        cursor.execute("INSERT INTO utilisateurs (username, email, password, face_descriptor) VALUES (?, ?, ?, ?)",
                       (username, email, hashed_pw, blob))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return "duplicate"
    except Exception as e:
        print("Erreur à l'inscription :", e)
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    cursor.execute("SELECT * FROM utilisateurs WHERE username = ? AND password = ?", (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return user

def match_face(current_desc, threshold=0.7):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, face_descriptor FROM utilisateurs WHERE face_descriptor IS NOT NULL")
    distances = []
    for username, face_blob in cursor.fetchall():
        if face_blob:
            face_saved = pickle.loads(face_blob)
            distance = np.linalg.norm(current_desc - face_saved)
            print(f"👤 {username} → distance : {distance:.4f}")
            distances.append((username, distance))
    conn.close()
    if not distances:
        print("❌ Aucun utilisateur encodé")
        return None
    distances.sort(key=lambda x: x[1])
    best_user, best_distance = distances[0]
    print(f"🎯 Plus proche : {best_user} à {best_distance:.4f}")
    if best_distance < threshold:
        return best_user
    return None
