import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
from PIL import Image, ImageTk
from app.face_detector import detect_and_crop_face
from app.recognizer import FaceRecognizer
from app.student_data import get_student_by_label
from app.corrections import save_correction
from app.attendance import mark_attendance

class FRASApp:
    def __init__(self, window):
        self.window = window
        self.window.title("FRAS - Face Recognition Attendance")
        self.vid = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()
        
        # 1. New Scan Button
        self.btn_scan = tk.Button(window, text="1. Scan Face", command=self.scan_face, bg="lightblue", font=("Arial", 12, "bold"))
        self.btn_scan.pack(side=tk.TOP, padx=20, pady=5)
        
        self.btn_confirm = tk.Button(window, text="2. Confirm Identity", command=self.confirm_identity)
        self.btn_confirm.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.btn_manual = tk.Button(window, text="Manual Match", command=self.manual_match)
        self.btn_manual.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.recognizer = FaceRecognizer()
        self.current_frame = None
        self.current_label = None
        self.is_recognized = False
        
        # 2. Flag to pause the video feed after scanning
        self.is_paused = False
        
        self.update_frame()
        
    def update_frame(self):
        # Only update the camera feed if we aren't paused on a scanned face
        if not self.is_paused:
            ret, frame = self.vid.read()
            if ret:
                self.current_frame = frame.copy()
                cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
        self.window.after(15, self.update_frame)
        
    def scan_face(self):
        if self.current_frame is None:
            messagebox.showerror("Error", "Camera not ready.")
            return

        self.is_paused = True
        
        # Flip the frame left-to-right to match Teachable Machine's browser mirror!
        mirrored_frame = cv2.flip(self.current_frame, 1)
        display_frame = mirrored_frame.copy()
        
        # Feed the FULL mirrored frame directly to the AI
        self.is_recognized, self.current_label, confidence = self.recognizer.predict_face(mirrored_frame)
        
        # Draw the result on the top-left corner
        color = (0, 255, 0) if self.is_recognized else (0, 0, 255)
        display_text = f"{self.current_label} ({confidence:.2f})" if self.is_recognized else "Unknown"
        cv2.putText(display_frame, display_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
        
        # Update canvas
        cv_img = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        # Notify user
        if self.is_recognized:
            messagebox.showinfo("Scan Complete", f"AI matched: {self.current_label}\nClick 'Confirm Identity' if this is correct.")
        else:
            messagebox.showwarning("Unrecognized", "AI could not recognize you. Please click 'Manual Match'.")
            
    def confirm_identity(self):
        if self.is_recognized and self.current_label:
            student_info = get_student_by_label(self.current_label)
            name = student_info.get("name", self.current_label) if student_info else self.current_label
            mark_attendance(name)
            messagebox.showinfo("Confirmed", f"Attendance marked for {name}.")
            
            # Reset for the next student
            self.is_paused = False
            self.current_label = None
            self.is_recognized = False
        else:
            messagebox.showwarning("Warning", "Face not recognized. Please use Manual Match.")

    def manual_match(self):
        nickname = simpledialog.askstring("Manual Match", "Enter your nickname (label):", parent=self.window)
        if nickname:
            student_info = get_student_by_label(nickname.strip())
            if student_info:
                name = student_info.get("name", "Unknown")
                label = student_info.get("label", nickname.strip())
                if self.current_frame is not None:
                    save_correction(self.current_frame, label)
                mark_attendance(name)
                messagebox.showinfo("Success", f"Attendance marked for {name} and correction saved.")
                
                # Reset for the next student
                self.is_paused = False
                self.current_label = None
                self.is_recognized = False
            else:
                messagebox.showerror("Error", f"No student found with nickname '{nickname}'.")
                self.is_paused = False