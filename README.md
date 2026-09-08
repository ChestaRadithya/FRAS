# FRAS - Face Recognition Attendance System
FRAS is an automated, AI-driven attendance tracking application using Google Teachable Machine and OpenCV.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your exported `keras_model.h5` and `labels.txt` to the `model/` folder.
3. Update `data/students.json` with your student identities.

## Usage
* **Run the app**: `python main.py`
* **Collect new data**: `python scripts/capture_headshots.py`