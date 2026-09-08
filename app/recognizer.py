import numpy as np
import cv2
import os
from keras.models import load_model

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
                    
    def predict_face(self, cropped_face, confidence_threshold=0.85):
        if self.model is None:
            return False, "Model Not Loaded", 0.0

        # 1. Resize to 224x224 as required by Teachable Machine
        resized_image = cv2.resize(cropped_face, (224, 224), interpolation=cv2.INTER_AREA)
        
        # 2. Make it a numpy array and reshape
        image_array = np.asarray(resized_image, dtype=np.float32).reshape(1, 224, 224, 3)
        
        # 3. Normalize the image array from [0, 255] to [-1, 1]
        normalized_image_array = (image_array / 127.5) - 1.0
        
        # 4. Run prediction
        prediction = self.model.predict(normalized_image_array, verbose=0)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]
        
        # 5. Determine if recognized based on flowchart logic
        if confidence_score >= confidence_threshold and class_name.lower() != "unknown":
            return True, class_name, confidence_score
        else:
            return False, class_name, confidence_score