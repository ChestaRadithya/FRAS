import json
import os

def get_student_by_label(label_query):
    json_path = "data/students.json"
    if not os.path.exists(json_path):
        return None
        
    with open(json_path, 'r') as file:
        try:
            students_data = json.load(file)
            for student in students_data:
                if student.get("label", "").lower() == label_query.lower():
                    return student
        except json.JSONDecodeError:
            pass
    return None