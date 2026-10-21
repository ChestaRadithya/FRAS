import os
import cv2

def save_correction(frame, label):
    base_dir = "corrections"
    student_dir = os.path.join(base_dir, label)
    os.makedirs(student_dir, exist_ok=True)
    
    existing_files = os.listdir(student_dir)
    correction_files = [f for f in existing_files if f.startswith("correction_")]
    incremental_number = len(correction_files) + 1
    
    filename = f"correction_{incremental_number}.jpg"
    file_path = os.path.join(student_dir, filename)
    
    success = cv2.imwrite(file_path, frame)
    return success