import numpy as np
import cv2
import os
from keras.models import load_model
from PIL import Image, ImageOps

class FaceRecognizer:
    def __init__(self, model_path="model/keras_model.h5", labels_path="model/labels.txt"):
        if not os.path.exists(model_path) or not os.path.exists(labels_path):
            print("Error: Model files not found.")
            self.model = None
            return

        np.set_printoptions(suppress=True)
        
        # Load the model directly using Keras
        self.model = load_model(model_path, compile=False)
        
        # Load the labels (This is what was missing!)
        self.class_names = []
        with open(labels_path, "r") as f:
            for line in f.readlines():
                parts = line.strip().split(" ", 1)
                if len(parts) == 2:
                    self.class_names.append(parts[1])
                else:
                    self.class_names.append(parts[0])
                    
    def predict_face(self, frame, confidence_threshold=0.60):
        if self.model is None:
            return False, "Model Not Loaded", 0.0

        # 1. Convert OpenCV BGR to RGB and transform into a PIL Image
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        
        # 2. Mimic TM's exact center-crop and resize using LANCZOS interpolation
        size = (224, 224)
        image = ImageOps.fit(pil_image, size, Image.Resampling.LANCZOS)
        
        # 3. Turn the image into a numpy array and normalize it
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1.0
        
        # 4. Load into the data array
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array
        
        # 5. Run prediction
        prediction = self.model.predict(data, verbose=0)

        # --- NEW DIAGNOSTIC CODE ---
        print("\n--- AI Brain Scan ---")
        for i, name in enumerate(self.class_names):
            print(f"{name}: {prediction[0][i]*100:.2f}%")
        print("---------------------")
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]
        
        if confidence_score >= confidence_threshold and class_name.lower() != "unknown":
            return True, class_name, confidence_score
        else:
            return False, class_name, confidence_score