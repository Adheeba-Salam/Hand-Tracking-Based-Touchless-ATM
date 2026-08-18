import face_recognition
import os
from config import cfg
from database import Database

class FaceRec:
    def __init__(self, facespath="./Faces"):
        self.db = Database()
        self.faces = {}
        
        # Load and encode all faces from the database
        for file in os.listdir(facespath):
            if file.endswith(".jpeg") or file.endswith(".jpg"):
                img_path = os.path.join(facespath, file)
                img = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(img)
                if encodings:
                    self.faces[file] = encodings[0]

    def MatchTheFace(self, img):
        """Match the face in the current frame with the database"""
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            return False, None, None  # No face detected
        
        for user_face, stored_encoding in self.faces.items():
            if face_recognition.compare_faces([stored_encoding], encodings[0], tolerance=cfg["tolerance"])[0]:
                user = self.db.get_user_by_face(user_face)
                if user:
                    return True, user[0], user[1]  # Return match status, user ID, and user name
        
        return False, None, None