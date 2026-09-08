import cv2

def detect_and_crop_face(frame):
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(150, 150))
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cropped_face = frame[y:y+h, x:x+w]
        return True, cropped_face, (x, y, w, h)
        
    return False, None, None