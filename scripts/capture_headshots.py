import cv2
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.face_detector import detect_and_crop_face

def capture_dataset():
    label = input("Enter the student's nickname/label: ").strip().lower()
    if not label: return

    save_dir = os.path.join("dataset", label)
    os.makedirs(save_dir, exist_ok=True)
    
    time.sleep(2)
    vid = cv2.VideoCapture(0)
    count = 0
    max_captures = 100

    while count < max_captures:
        ret, frame = vid.read()
        if not ret: break
            
        face_found, cropped_face, bbox = detect_and_crop_face(frame)
        display_frame = frame.copy()
        
        if face_found:
            filename = os.path.join(save_dir, f"{label}_{count:04d}.jpg")
            cv2.imwrite(filename, cropped_face)
            count += 1
            x, y, w, h = bbox
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(display_frame, f"Captured: {count}/{max_captures}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Dataset Collection", display_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    vid.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_dataset()