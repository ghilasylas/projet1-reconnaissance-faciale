
import face_recognition

def detect_face_descriptor(image):
    encodings = face_recognition.face_encodings(image)
    if encodings:
        return encodings[0]
    return None
